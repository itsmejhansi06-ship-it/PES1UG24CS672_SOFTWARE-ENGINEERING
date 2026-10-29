
from ski_resort_pass import (
    process_resort_bookings,
    check_chairlift_anemometer,
)


def test_groups_validation_branches():
    try:
        process_resort_bookings("invalid", 0)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        process_resort_bookings([], -1)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_active_and_inactive_groups():
    groups = [
        {"is_active": False},
        {"is_active": True, "duration": "full_day",
         "skiers": [{"age": 30}]},
    ]
    result = process_resort_bookings(groups, 0)
    assert result["total_revenue"] == 80.0


def test_all_duration_branches():
    groups = [
        {"is_active": True, "duration": "season",
         "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "full_day",
         "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "half_day",
         "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "unknown",
         "skiers": [{"age": 30}]},
    ]
    result = process_resort_bookings(groups, 0)
    assert result["total_revenue"] == 430.0


def test_age_branches():
    groups = [{
        "is_active": True,
        "duration": "full_day",
        "skiers": [
            {"age": 0},
            {"age": 10},
            {"age": 65},
            {"age": 30},
        ],
    }]
    result = process_resort_bookings(groups, 0)
    assert result["total_revenue"] == 184.0


def test_blackout_branches():
    groups = [
        {"is_active": True, "duration": "full_day",
         "skiers": [{"age": 30, "blackout_override": True}]},
        {"is_active": True, "duration": "half_day",
         "skiers": [
             {"age": 30},
             {"age": 30, "blackout_override": True},
         ]},
    ]
    result = process_resort_bookings(groups, 0)
    assert result["total_revenue"] == 40.0


def test_gear_and_locker_branches():
    groups = [
        {"is_active": True, "duration": "full_day",
         "skiers": [{"age": 30, "gear_rental": True}],
         "includes_lodge_locker": True},
        {"is_active": True, "duration": "half_day",
         "skiers": [{"age": 30, "gear_rental": False}],
         "includes_lodge_locker": False},
    ]
    result = process_resort_bookings(groups, 10)
    assert result["total_revenue"] == 175.0


def test_status_branches():
    assert process_resort_bookings([], 0)["status"] == "ZERO_SALES"

    invalid_skiers = [{"age": 0} for _ in range(5)]
    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": invalid_skiers}], 0
    )
    assert result["status"] == "AUDIT_REVIEW"

    result = process_resort_bookings(
        [{"is_active": True, "duration": "full_day",
          "skiers": [{"age": 30}]}], 0
    )
    assert result["status"] == "COMPLETED"


def test_wind_branches():
    assert check_chairlift_anemometer([]) == "NO_DATA"
    assert check_chairlift_anemometer([[20, 30, 45]]) == "SAFE_OPERATION"
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"
    assert check_chairlift_anemometer([[46, 20, 47]]) == "SAFE_OPERATION"
