from copy import deepcopy

from db.atomictransaction import AtomicTransaction
from db.models.main_object import MainObject
from unittest import TestCase


def test_transaction():

    finger_print = deepcopy(MainObject._BaseStorage__storage)
    expected_value = {
        'MainObject':
            {
                2: {'id': 2, 'value': 'random_data'},
                3: {'id': 3, 'value': 'random_data'},
                4: {'id': 4, 'value': 'random_data'}
            },
        **finger_print
    }
    with AtomicTransaction() as transaction:
        with transaction as transaction:
            transaction.begin(
                (MainObject.create, {"value": {"value": "random_data"}}),
                (MainObject.create, {"value": {"value": "random_data"}}),
            )
        transaction.begin(
            (MainObject.create, {"value": {"value": "random_data"}}),
            (MainObject.create, {"value": {"value": "random_data"}}),
            (MainObject.delete, {"deleted_id": 800}),
            (MainObject.delete, {"deleted_id": 1}),
        )
    TestCase().assertDictEqual(MainObject._BaseStorage__storage, expected_value)


def test_error_in_last_transaction_level():
    expected_value = deepcopy(MainObject._BaseStorage__storage)
    with AtomicTransaction() as transaction:
        with transaction as transaction:
            transaction.begin(
                (MainObject.create, {"value": {"value": "random_data"}}),
                (MainObject.create, {"value": {"value": "random_data"}}),
            )
        transaction.begin(
            (MainObject.create, {"value": {"value": "random_data"}}),
            (MainObject.create, {"value": {"value": "random_data"}}),
            (MainObject.delete, {"random": "asd"}),
        )
    TestCase().assertDictEqual(MainObject._BaseStorage__storage, expected_value)


def test_create():
    created_object = MainObject.create({"id": 8000, "value": "random"})
    assert created_object.id == 8000
    assert created_object.value == "random"

    created_object = MainObject.create({"value": "random"})
    assert created_object.id == 8001
    assert created_object.value == "random"


def test_get():
    fingerprint = deepcopy(MainObject._BaseStorage__storage)
    expected_value = [MainObject(**fingerprint['MainObject'][value]) for value in fingerprint['MainObject']]
    assert expected_value == MainObject.get()


def test_delete():
    created_object = MainObject.create({"id": 9000, "value": "random"})
    assert created_object == MainObject.get(9000)[0]
    MainObject.delete(deleted_id=created_object.id)
    assert MainObject.get(9000) ==  []
