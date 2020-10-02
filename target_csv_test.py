import target_csv
import unittest


class TestTargetCsv(unittest.TestCase):

  def setUp(self):
    pass

  def test_get_headers(self):
    schema = {"properties": {
      'a': {'type': 'string'},
      'b': {'type': 'array', 'items': {'type': 'string'}},
      'c': {'type': 'object', 'properties': {'d': {'type': 'string'}}}
    }}

    assert target_csv.get_headers(schema) == ['a', 'b', 'c__d']

  def test_get_headers_matches_flatten(self):
    schema = {'properties': {
      'a': {'type': 'string'},
      'b': {'type': 'array', 'items': {'type': 'string'}},
      'c': {'type': 'object', 'properties': {'d': {'type': 'string'}}}
    }}

    record = {
      'a': 'alpha',
      'b': ['beta'],
      'c': {'d': 'delta'}
    }

    keys_from_schema = target_csv.get_headers(schema)
    keys_from_records = list(target_csv.flatten(record).keys())
    assert keys_from_schema == keys_from_records

if __name__ == '__main__':
  unittest.main()
