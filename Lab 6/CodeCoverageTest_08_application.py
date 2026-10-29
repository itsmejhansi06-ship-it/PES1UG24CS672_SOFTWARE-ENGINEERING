
import pytest

from ski_resort_pass import (
    process_resort_bookings,
    check_chairlift_anemometer,
)


def test_invalid_groups():
    with pytest.raises(ValueError):
        process_resort_bookings("invalid", 0)


def test_negative_facility_fee():
    with pytest.raises(ValueError):
        process_resort_bookings([], -1)


def test_empty_groups():
    assert process_resort_bookings([], 0) == {
        "total_revenue": 0.0,
        "status": "ZERO_SALES",
    }


def test_inactive_group():
    result = process_resort_bookings(
        [{"is_active": False}], 10
    )
    assert result["status"] == "ZERO_SALES"


def test_all_pass_durations():
    groups = [
        {"is_active": True, "duration": "season",
         "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "full_day",
         "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "half_day",
         "skiers": [{"age": 30}]},
    ]
    result = process_resort_bookings(groups, 0)
    assert result == {
        "total_revenue": 430.0,
        "status": "COMPLETED",
    }


def test_invalid_duration():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "weekly",
          "skiers": [{"age": 30}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_child_discount():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": [{"age": 10}]}], 0
    )
    assert result["total_revenue"] == 48.0


def test_senior_discount():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": [{"age": 70}]}], 0
    )
    assert result["total_revenue"] == 56.0


def test_regular_adult():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": [{"age": 30}]}], 0
    )
    assert result["total_revenue"] == 80.0


def test_invalid_age_is_rejected():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": [{"age": 0}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_gear_rental():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": [{"age": 30, "gear_rental": True}]}], 0
    )
    assert result["total_revenue"] == 115.0


def test_locker_fee():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "half_day",
          "skiers": [{"age": 30}],
          "includes_lodge_locker": True}], 20
    )
    assert result["total_revenue"] == 70.0


def test_blackout_override():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": [{"age": 30, "blackout_override": True}]}], 0
    )
    assert result["total_revenue"] == 40.0


def test_half_day_blackout_cancels_group_total():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "half_day",
          "skiers": [
              {"age": 30},
              {"age": 30, "blackout_override": True},
              {"age": 30},
          ]}], 0
    )
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_SALES"


def test_audit_review():
    skiers = [{"age": 0} for _ in range(5)]
    skiers.append({"age": 30})
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": skiers}], 0
    )
    assert result["total_revenue"] == 80.0
    assert result["status"] == "AUDIT_REVIEW"


def test_empty_wind_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_safe_wind():
    assert check_chairlift_anemometer(
        [[20, 30, 45, 25]]
    ) == "SAFE_OPERATION"


def test_two_consecutive_dangerous_gusts():
    assert check_chairlift_anemometer(
        [[46, 50]]
    ) == "SUSPEND_LIFT"


def test_gusts_interrupted_by_safe_wind():
    assert check_chairlift_anemometer(
        [[50, 30, 50]]
    ) == "SAFE_OPERATION"


def test_dangerous_gusts_in_separate_readings():
    assert check_chairlift_anemometer(
        [[50], [51]]
    ) == "SAFE_OPERATION"
