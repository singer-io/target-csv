import target_csv
import json


def test_flatten_empty():
    x = target_csv.flatten({})
    assert x == {}


def test_flatten_simple():
    x = target_csv.flatten({"f1": 1, "f2": "string", "f3": None, "f4": False})
    assert x == {"f1": 1, "f2": "string", "f3": None, "f4": False}


def test_flatten_list_simple():
    x = target_csv.flatten({"wrap": ["string", 1, None, False]})
    # Previous implementation produced invalid json:
    #   {"warp": "['string', 1, None, False]"}

    json.loads(x['wrap'])
    assert x == {"wrap": '["string", 1, null, false]'}


def test_flatten_list_complex():
    x = target_csv.flatten({"wrap": [{"n": 1}, {"n": 2}]})

    json.loads(x['wrap'])
    assert x == {"wrap": '[{"n": 1}, {"n": 2}]'}


def test_flatten_list_complex_non_ascii():
    x = target_csv.flatten({
        "wrap": [
            {
                "japanese": "私の問題を",
                "russian": "Удовлетворены"
            }
        ]})

    json.loads(x['wrap'])
    assert x == {"wrap": '[{"japanese": "私の問題を", "russian": "Удовлетворены"}]'}
