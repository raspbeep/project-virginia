import pytest
from classes import *


@pytest.mark.parametrize("amount, currency, merchant, status_code", [("5", "EUR", "merchant", 200), ("x", "EUR", "zlavomat", 200)])
def test_P1(amount, currency, merchant, status_code):
    prov = P1()
    assert prov.pay(amount, currency, merchant) == status_code


@pytest.mark.parametrize("amount, currency, merchant, status_code", [("5", "EUR", "merchant", 200), ("x", "EUR", "zlavomat", 69)])
def test_P2(amount, currency, merchant, status_code):
    prov = P2()
    assert prov.pay(amount, currency, merchant) == status_code


@pytest.mark.parametrize("amount, currency, merchant, status_code", [("5", "EUR", "merchant", 200), ("x", "EUR", "zlavomat", 69)])
def test_P3(amount, currency, merchant, status_code):
    prov = P3()
    assert prov.pay(amount, currency, merchant) == status_code
