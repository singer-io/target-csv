#!/usr/bin/env python3

import argparse
import io
import os
import sys
import json
import csv
import threading
import http.client
import urllib
from datetime import datetime
import collections
import pkg_resources
import shutil

from jsonschema.validators import Draft4Validator
import singer

logger = singer.get_logger()

def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()

def flatten(d, parent_key='', sep='__'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v) if type(v) is list else v))
    return dict(items)

def persist_messages(delimiter, quotechar, messages, destination_path, rewrite_headers):
    state = None
    schemas = {}
    key_properties = {}
    headers = {}
    validators = {}
    files_incorrect_headers = {}  # Keep track of files with incorrect headers

    now = datetime.now().strftime('%Y%m%dT%H%M%S')

    for message in messages:
        try:
            o = singer.parse_message(message).asdict()
        except json.decoder.JSONDecodeError:
            logger.error("Unable to parse:\n{}".format(message))
            raise
        message_type = o['type']
        if message_type == 'RECORD':
            stream = o['stream']
            if stream not in schemas:
                raise Exception("A record for stream {}"
                                "was encountered before a corresponding schema".format(stream))

            validators[stream].validate(o['record'])

            filename = stream + '-' + now + '.csv'
            filename = os.path.expanduser(os.path.join(destination_path, filename))
            file_is_empty = (not os.path.isfile(filename)) or os.stat(filename).st_size == 0

            flattened_record = flatten(o['record'])

            if stream not in headers:
                first_line = None
                if not file_is_empty:
                    with open(filename, 'r') as csv_f:
                        reader = csv.reader(csv_f,
                                            delimiter=delimiter,
                                            quotechar=quotechar)
                        first_line = next(reader)
                headers[stream] = first_line if first_line else list(flattened_record.keys())

            # Check current record for unseen field.
            missing_header_fields = set(flattened_record.keys()).difference(headers[stream])

            if missing_header_fields:
                headers[stream] += missing_header_fields
                files_incorrect_headers[filename] = headers[stream]

            with open(filename, 'a') as csvfile:
                writer = csv.DictWriter(csvfile,
                                        headers[stream],
                                        extrasaction='ignore',
                                        delimiter=delimiter,
                                        quotechar=quotechar)
                if file_is_empty:
                    writer.writeheader()

                writer.writerow(flattened_record)

            state = None
        elif message_type == 'STATE':
            logger.debug('Setting state to {}'.format(o['value']))
            state = o['value']
        elif message_type == 'SCHEMA':
            stream = o['stream']
            schemas[stream] = o['schema']
            validators[stream] = Draft4Validator(o['schema'])
            key_properties[stream] = o['key_properties']
        else:
            logger.warning("Unknown message type {} in message {}"
                           .format(o['type'], o))

    if files_incorrect_headers and rewrite_headers.lower() == 'true':
        rewrite_csv(files_incorrect_headers, delimiter, quotechar)

    return state


def rewrite_csv(files_incorrect_headers, delimiter, quotechar):
    """
    Rewrite the CSV-file(s) to update the first line, the header.

    Thereby duplicate the data and overwrite the original file afterwards.
    """
    logger.info('Rewriting {} csv file(s) with incorrect headers.'
                .format(len(files_incorrect_headers)))

    for filename, correct_header in files_incorrect_headers.items():
        tmp_filename = filename + ".tmp"

        with open(filename, "r") as csv_f:
            csv_f.readline()  # ignore the incorrect header

            with open(tmp_filename, "w") as tmp_f:
                writer = csv.DictWriter(tmp_f,
                                        correct_header,
                                        extrasaction='ignore',
                                        delimiter=delimiter,
                                        quotechar=quotechar)
                # Write correct headers and rest of the content.
                writer.writeheader()
                shutil.copyfileobj(csv_f, tmp_f)

        # Atomic move after updating file
        shutil.move(tmp_filename, filename)


def send_usage_stats():
    try:
        version = pkg_resources.get_distribution('target-csv').version
        conn = http.client.HTTPConnection('collector.singer.io', timeout=10)
        conn.connect()
        params = {
            'e': 'se',
            'aid': 'singer',
            'se_ca': 'target-csv',
            'se_ac': 'open',
            'se_la': version,
        }
        conn.request('GET', '/i?' + urllib.parse.urlencode(params))
        response = conn.getresponse()
        conn.close()
    except:
        logger.debug('Collection request failed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as input_json:
            config = json.load(input_json)
    else:
        config = {}

    if not config.get('disable_collection', False):
        logger.info('Sending version information to singer.io. ' +
                    'To disable sending anonymous usage data, set ' +
                    'the config parameter "disable_collection" to true')
        threading.Thread(target=send_usage_stats).start()

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    state = persist_messages(config.get('delimiter', ','),
                             config.get('quotechar', '"'),
                             input_messages,
                             config.get('destination_path', ''),
                             config.get('rewrite_headers', False))

    emit_state(state)
    logger.debug("Exiting normally")


if __name__ == '__main__':
    main()
