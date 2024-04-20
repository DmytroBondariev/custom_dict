import pytest

from custom_dict import Dictionary


def test_basic_operations():
    dictionary = Dictionary()
    dictionary["key1"] = "value1"
    dictionary["key2"] = "value2"
    assert dictionary["key1"] == "value1"
    assert dictionary["key2"] == "value2"
    assert len(dictionary) == 2


def test_updating_values():
    dictionary = Dictionary()
    dictionary["key1"] = "value1"
    dictionary["key1"] = "new_value1"
    assert dictionary["key1"] == "new_value1"


def test_non_existent_keys_and_resizing():
    dictionary = Dictionary()

    with pytest.raises(KeyError):
        _ = dictionary["key1"]

    for i in range(100):
        dictionary[f"key{i}"] = f"value{i}"
    assert len(dictionary) == 100
    assert dictionary["key99"] == "value99"


def test_collision_same_hash_keys():
    dictionary = Dictionary()

    dictionary[10] = "value1"
    dictionary[10.0] = "value2"

    assert dictionary[10] == "value1"
    assert dictionary[10.0] == "value2"


def test_memory_usage_and_deletion():
    dictionary = Dictionary()

    for i in range(100):
        dictionary[f"key{i}"] = f"value{i}"

    assert len(dictionary) == 100
    assert dictionary.capacity == 256

    for i in range(50):
        del dictionary[f"key{i}"]

    assert len(dictionary) == 50
    assert dictionary.capacity == 128


def test_load_factor_edge_changes():
    dictionary = Dictionary(initial_capacity=8, load_factor=0.75)

    for i in range(7):
        dictionary[f"key{i}"] = f"value{i}"

    assert len(dictionary) == 7
    assert dictionary.capacity == 16

    for i in range(4):
        del dictionary[f"key{i}"]

    assert len(dictionary) == 3
    assert dictionary.capacity == 8


def test_multiple_kwargs_init():
    dictionary = Dictionary(key1="value1", key2="value2", key3="value3", key4="value4", key5="value5",
                            key6="value6", key7="value7", key8="value8", key9="value9", key10="value10")

    assert len(dictionary) == 10
    for index in range(10):
        assert dictionary[f'key{index + 1}'] == f'value{index + 1}'
        assert [(f"key{index + 1}", f"value{index + 1}", hash(f'key{index + 1}'))] in dictionary.buckets


def test_contains_method():
    dictionary = Dictionary()
    dictionary["key1"] = "value1"
    dictionary["key2"] = "value2"

    assert "key1" in dictionary
    assert "key2" in dictionary
    assert "key3" not in dictionary
