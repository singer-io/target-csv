import target_csv


def test_flatten_empty():
    x = target_csv.flatten({})
    assert x == {}


def test_flatten_simple():
    x = target_csv.flatten({"f1": 1})
    assert x == {"f1": 1}


def test_flatten_list_simple():
    x = target_csv.flatten({"f1": ["1", "2", 3]})
    assert x == {"f1": '["1", "2", 3]'}


def test_flatten_list_complex():
    x = target_csv.flatten({"f1": [{"n": 1}, {"n": 2}]})
    assert x == {"f1": '[{"n": 1}, {"n": 2}]'}


def test_flatten_list_complex_non_ascii():
    x = target_csv.flatten(
        {"f1": [
            {"japanese": "私の問題を",
             "russian": "Удовлетворены"}]
        })
    assert x == {"f1": '[{"japanese": "私の問題を", "russian": "Удовлетворены"}]'}
