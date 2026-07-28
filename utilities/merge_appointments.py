# Independent utility script
import csv
from pathlib import Path


def merge_appointment_files(primary_path: str, secondary_path: str, output_path: str) -> None:
    """Adds new appointments by cross-referencing old appointments in previous CSV appointment file to avoid needing to export multiple times from CRM (return to this)."""
    p_file = Path(primary_path)
    s_file = Path(secondary_path)
    o_file = Path(output_path)

    if not p_file.exists() or not s_file.exists():
        print("Missing required input CSV files for merge operation.")
        return

    merged_records = []
    seen_ids = set()

    for file_path in (p_file, s_file):
        with open(file_path, mode='r', encoding='utf-8-sig') as stream:
            reader = csv.DictReader(stream)
            for row in reader:
                donation_id = row.get('Donation ID', '').strip()
                if donation_id and donation_id not in seen_ids:
                    seen_ids.add(donation_id)
                    merged_records.append(row)

    if not merged_records:
        print("No valid appointment records found to merge.")
        return

    fieldnames = list(merged_records[0].keys())
    o_file.parent.mkdir(parents=True, exist_ok=True)

    with open(o_file, mode='w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_records)

    print(f"Successfully merged {len(merged_records)} unique records into: {output_path}")


if __name__ == "__main__":
    # Example execution fallback when running script directly from command line
    merge_appointment_files(
        primary_path="inputs/appointments_raw.csv",
        secondary_path="inputs/appointments_update.csv",
        output_path="inputs/appointments.csv"
    )