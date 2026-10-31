"""Tests that exercise both outcomes of electricity_bill.py decisions."""

import pytest

from electricity_bill import energy_charge, late_fee, subsidy


@pytest.mark.parametrize(
    ("units", "connection", "expected"),
    [
        (50, "domestic", 200),       # <= 100; not commercial
        (101, "domestic", 355),      # > 100 and <= 300
        (301, "domestic", 1358),     # > 300
        (50, "commercial", 450),    # commercial multiplier
    ],
)
def test_energy_charge_success_branches(units, connection, expected):
    assert energy_charge(units, connection) == expected


@pytest.mark.parametrize(
    ("units", "connection", "message"),
    [
        (50, "unknown", "unknown connection"),
        (-1, "domestic", "invalid units"),
    ],
)
def test_energy_charge_error_branches(units, connection, message):
    with pytest.raises(ValueError, match=message):
        energy_charge(units, connection)


@pytest.mark.parametrize(
    ("bill", "days_late", "expected"),
    [
        (500, 0, 0),       # days_late <= 0
        (500, 15, 50),     # 0 < days_late <= 15
        (2000, 16, 100),   # over 15 days, bill is not over 2000
        (2001, 16, 200),   # over 15 days and bill is over 2000
    ],
)
def test_late_fee_branches(bill, days_late, expected):
    assert late_fee(bill, days_late) == expected


@pytest.mark.parametrize(
    ("units", "is_senior", "has_solar", "expected"),
    [
        (100, True, False, 50),    # units <= 100 and senior
        (100, False, False, 0),    # units <= 100 and not senior
        (101, True, False, 0),     # units > 100
        (50, False, True, 100),    # solar, units <= 300
        (50, True, True, 150),     # senior plus solar
        (301, True, True, 0),      # solar and units > 300 resets amount
        (301, False, False, 0),    # no solar
    ],
)
def test_subsidy_branches(units, is_senior, has_solar, expected):
    assert subsidy(units, is_senior, has_solar) == expected
