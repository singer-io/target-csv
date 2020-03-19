import target_csv


def test_flatten_empty():
    res = target_csv.flatten({})
    assert res == {}


def test_flatten_simple():
    res = target_csv.flatten({"f1": 1})
    assert res == {"f1": 1}


def test_flatten_list_simple():
    res = target_csv.flatten({"f1": ["1", "2", 3]})
    assert res == {"f1": '["1", "2", 3]'}


def test_flatten_list_complex():
    res = target_csv.flatten({"f1": [{"n": 1}, {"n": 2}]})
    assert res == {"f1": '[{"n": 1}, {"n": 2}]'}


def test_flatten_list_complex_non_ascii():
    res = target_csv.flatten({"f1": [{"japanese": "私の問題を", "russian": "Удовлетворены"}]})
    assert res == {"f1": '[{"japanese": "私の問題を", "russian": "Удовлетворены"}]'}
