# py -3 tests\mytest.py


import pytest
from tests.calculations import add, substract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account(): 
  return BankAccount(0)

@pytest.fixture
def fifty_bank_account():
  return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3), (3, 4, 7), (4, 6, 10)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_substract():
    assert substract(1, 2) == -1


def test_multiply():
    assert multiply(1, 2) == 2


def test_divide():
    assert divide(1, 2) == 0.5


def test_bank_account_set_initial_balance(zero_bank_account, fifty_bank_account):
    #bank_account = BankAccount(10) don't need this anymore since we passed the fixture as arg 
    assert zero_bank_account.balance == 0
    assert fifty_bank_account.balance == 50
