# CSV generation logic
import csv
from datetime import datetime
from typing import List, Any


def generate_cell_line_csv_report(filename: str, donor_list: List[Any]) -> None:
    """Compiles and exports cell line candidate records into a formatted CSV file."""
    headers = [
        "Scheduled? (Y/N)", "Date Scheduled", "Donor ID", "IDS Expiry", "Blood Type", 
        "Date of Birth", "Age", "Sex", "Ethnicity", "Donation Types", "BMI", 
        "Taking Daily Meds? (Y/N)", "Tobacco Use", "CMV Status", "EBV Status", 
        "Reliability Score"
    ]

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=headers)
            writer.writeheader()

            for donor in donor_list:
                # Format dates safely
                expiry_str = donor.last_ids_expiry.strftime('%m/%d/%Y') if isinstance(donor.last_ids_expiry, datetime) else str(donor.last_ids_expiry or 'N/A')
                dob_str = donor.date_of_birth.strftime('%m/%d/%Y') if isinstance(donor.date_of_birth, datetime) else str(donor.date_of_birth)

                taking_meds_str = 'Y' if donor.taking_daily_meds else 'N'
                tobacco_use_str = 'Y' if donor.tobacco_use else 'N'
                
                # Safeguard string formatting against optional None values
                cmv_val = donor.cmv_igg or ''
                ebv_val = donor.ebv_igg or ''
                cmv_str = cmv_val.strip().lower().title() if cmv_val else 'N/A'
                ebv_str = ebv_val.strip().lower().title() if ebv_val else 'N/A'

                donation_types_str = ", ".join(donor.donation_types) if isinstance(donor.donation_types, list) else str(donor.donation_types)

                # Check for upcoming appointments
                donor_history = donor.sorted_appointments.get(donor.donor_id, {})
                future_appts = donor_history.get('future', [])

                if future_appts:
                    scheduled_str = 'Y'
                    raw_appt_str = future_appts[0]
                    datetime_part = raw_appt_str.split('|')[0].strip()
                    try:
                        dt_obj = datetime.strptime(datetime_part, '%Y-%m-%d %H:%M:%S')
                        date_str = f"{dt_obj.month}/{dt_obj.day}/{dt_obj.year}"
                        time_str = dt_obj.strftime('%I:%M%p').lower().lstrip('0')
                        date_scheduled_str = f"{date_str} @ {time_str}"
                    except ValueError:
                        date_scheduled_str = datetime_part
                else:
                    scheduled_str = 'N'
                    date_scheduled_str = '-'

                row = {
                    "Scheduled? (Y/N)": scheduled_str,
                    "Date Scheduled": date_scheduled_str, 
                    "Donor ID": donor.donor_id,
                    "IDS Expiry": expiry_str,
                    "Blood Type": donor.blood_type,
                    "Date of Birth": dob_str,
                    "Age": donor.age,
                    "Sex": donor.sex,
                    "Ethnicity": donor.ethnicity,
                    "Donation Types": donation_types_str,
                    "BMI": donor.bmi,
                    "Tobacco Use": tobacco_use_str,
                    "CMV Status": cmv_str,
                    "EBV Status": ebv_str,
                    "Taking Daily Meds? (Y/N)": taking_meds_str,
                    "Reliability Score": donor.reliability_score
                }
                writer.writerow(row)

        print(f"Exported: {filename} ({len(donor_list)} records)")
    except Exception as err:
        print(f"Failed to generate report {filename}: {err}")