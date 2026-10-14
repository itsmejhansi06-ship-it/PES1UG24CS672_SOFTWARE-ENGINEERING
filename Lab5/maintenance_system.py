"""Maintenance asset registration and service tracking system."""

import json
import tempfile
from datetime import datetime, timedelta


assets = {}
SERVICE_INTERVAL_DAYS = 90


def register_asset(asset_id, machine_type, logs=None):
    """Register an asset and record its ID in the registration logs."""
    if logs is None:
        logs = []

    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime("%Y-%m-%d"),
    }
    logs.append(asset_id)
    print(
        "Registered",
        asset_id,
        "- total registrations this run:",
        len(logs),
    )


def update_service_date(asset_id, service_date):
    """Update an asset's last service date after validating the date."""
    if asset_id not in assets:
        print("Could not update", asset_id)
        return

    try:
        datetime.strptime(service_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid service date for", asset_id)
        return

    assets[asset_id]["last_service"] = service_date


def due_for_inspection(interval_days=SERVICE_INTERVAL_DAYS):
    """Return IDs of assets overdue for inspection."""
    due = []
    today = datetime.now()

    for asset_id, asset in assets.items():
        last_service = datetime.strptime(
            asset["last_service"], "%Y-%m-%d"
        )
        if today - last_service > timedelta(days=interval_days):
            due.append(asset_id)

    return due


def change_interval(days):
    """Return the service interval selected by the caller."""
    return days


def export_service_report(file="maintenance.json"):
    """Export asset details to a JSON report."""
    with open(file, "w", encoding="utf-8") as report:
        json.dump(assets, report, indent=2)

    print("Report written to " + file)


def write_scratch_copy():
    """Write asset details to a securely created temporary JSON file."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        encoding="utf-8",
        delete=False,
    ) as scratch_file:
        json.dump(assets, scratch_file)
        path = scratch_file.name

    print("Scratch copy at", path)


def print_alerts(interval_days=SERVICE_INTERVAL_DAYS):
    """Print alerts for assets overdue for inspection."""
    for asset_id in due_for_inspection(interval_days):
        print(
            "ALERT: inspection overdue for",
            asset_id,
            assets[asset_id]["type"],
        )


def main():
    """Run the maintenance system demonstration."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")

    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")

    interval_days = change_interval(-30)

    service_date = input(
        "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
    )
    if service_date:
        update_service_date("CV-07", service_date)

    if not assets:
        raise ValueError("No assets registered.")

    print_alerts(interval_days)
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
