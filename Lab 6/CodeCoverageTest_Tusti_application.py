"""Tests for line/code coverage of electricity_bill.py."""

import pytest

from electricity_bill import energy_charge, late_fee, subsidy


@pytest.mark.parametrize(
    ("units", "connection", "expected"),
    [
        (0, "domestic", 50),
        (50, "domestic", 200),
        (100, "domestic", 350),
        (101, "domestic", 355),
        (300, "domestic", 1350),
        (301, "domestic", 1358),
        (50, "commercial", 450),
        (101, "commercial", 760),
        (301, "commercial", 2766),
    ],
)
def test_energy_charge_calculations(units, connection, expected):
    assert energy_charge(units, connection) == expected


def test_energy_charge_rejects_unknown_connection():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(50, "industrial")


def test_energy_charge_rejects_negative_units():
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")


@pytest.mark.parametrize(
    ("bill", "days_late", "expected"),
    [
        (500, 0, 0),
        (500, -2, 0),
        (500, 1, 50),
        (500, 15, 50),
        (500, 16, 100),
        (2000, 16, 100),
        (2001, 16, 200),
    ],
)
def test_late_fee_calculations(bill, days_late, expected):
    assert late_fee(bill, days_late) == expected


@pytest.mark.parametrize(
    ("units", "is_senior", "has_solar", "expected"),
    [
        (100, True, False, 50),
        (100, False, False, 0),
        (101, True, False, 0),
        (50, False, True, 100),
        (50, True, True, 150),
        (301, True, True, 0),
        (301, False, False, 0),
    ],
)
def test_subsidy_calculations(units, is_senior, has_solar, expected):
    assert subsidy(units, is_senior, has_solar) == expected
