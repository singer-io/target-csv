#!/usr/bin/env python3

import argparse
import io
import os
import sys
import json
import csv

from jsonschema import validate
import singer

logger = singer.get_logger()


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()
        

def persist_lines(delimiter, quotechar, lines):
    """Takes a client and a stream and persists all the records to the gate,
    printing the state to stdout after each batch."""
    state = None
    schemas = {}
    key_properties = {}
    for line in lines:
        try:
            o = json.loads(line)
        except json.decoder.JSONDecodeError:
            logger.error("Unable to parse:\n{}".format(line))
            raise

        if 'type' not in o:
            raise Exception("Line is missing required key 'type': {}".format(line))
        t = o['type']

        if t == 'RECORD':
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))
            if o['stream'] not in schemas:
                raise Exception("A record for stream {} was encountered before a corresponding schema".format(o['stream']))

            schema = schemas[o['stream']]
            validate(o['record'], schema)

            top_level_fields = schema['properties'].keys()
            filename = o['stream'] + '.csv'

            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile,
                                        o['record'].keys(),
                                        delimiter=delimiter,
                                        quotechar=quotechar)
                if os.stat(filename).st_size == 0:
                    writer.writeheader()
                writer.writerow(o['record'])    

            state = None
        elif t == 'STATE':
            logger.debug('Setting state to {}'.format(o['value']))
            state = o['value']
        elif t == 'SCHEMA':
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))
            stream = o['stream']
            schemas[stream] = o['schema']
            if 'key_properties' not in o:
                raise Exception("key_properties field is required")
            key_properties[stream] = o['key_properties']
        else:
            raise Exception("Unknown message type {} in message {}"
                            .format(o['type'], o))

    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as input:
            config = json.load(input)
    else:
        config = {}

    input = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    state = None
    state = persist_lines(config.get('delimiter', ','),
                          config.get('quotechar', '"'),
                          input)
    emit_state(state)
    logger.debug("Exiting normally")


if __name__ == '__main__':
    main()
