# CSV generation logic
import csv
from datetime import datetime
from typing import List, Any
from src.models import Donor
from src.attribute_filter import get_ebv_donors


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
        
        
def generate_donor_demographics_csv_report(filename: str, donors: List[Donor]) -> None:
    """Compiles and exports donor demographics into a formatted CSV file."""
    # headers = ['Recallable', 'Donor ID', 'Age', 'Ethnicity', 'Sex', 'Tobacco Use', 'Blood Type', 'BMI', 'CMV Status']
    headers = ['Donor ID', 'Age', 'Ethnicity', 'Sex', 'Tobacco Use', 'Blood Type', 'BMI', 'CMV Status']
#  define headers
    try: 
        with open(filename, mode='w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=headers)
            writer.writeheader()
            
            for donor in donors:
                # IN APPS SCRIPTS, SKIP CMV IF NOT AVAILABLE
                tobacco_use_str = 'smoker' if donor.tobacco_use else 'non smoker'

                cmv_val = donor.cmv_igg or ''
                cmv_str = cmv_val.strip().lower() if cmv_val else ''
                
                row = {
                    # 'Recallable': donor.recallability_status,
                    'Donor ID': donor.donor_id,
                    'Age': donor.age,
                    'Ethnicity': donor.ethnicity.strip().lower(),
                    'Sex': donor.sex,
                    'Tobacco Use': tobacco_use_str,
                    'Blood Type': donor.blood_type,
                    'BMI': donor.bmi,
                    'CMV Status': cmv_str
                }
                writer.writerow(row)
        print(f"Exported {filename} ({len(donors)}) records)")
    except Exception as err:
        print(f"Failed to generate report {filename}: {err}")
        
# open csv dict writer
# iterate through each donor object
    # define variables required for csv file

def generate_final_appointment_report(filename: str, appointment_data: List[dict]) -> None:
    headers = ['Donor ID', 'Donation ID', 'Donation Type', 'Appointment Date', 'Appointment Time', 'Appointment Status', 'Donation Status', 'Appointment Subject']
    
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            
            for appointment in appointment_data:
                appointment_date_str = appointment['appointment_date'].strftime('%m/%d/%Y')
                appointment_time_str = appointment['appointment_time'].strftime('%I:%M%p').lower()
                
                row = {
                    'Donor ID': appointment['donor_id'],
                    'Donation ID': appointment['donation_id'],
                    'Donation Type': appointment['donation_type'],
                    'Appointment Date': appointment_date_str,
                    'Appointment Time': appointment_time_str,
                    'Appointment Status': appointment['appointment_status'],
                    'Donation Status': appointment['donation_status'],
                    'Appointment Subject': appointment['appointment_subject']
                }
                
                writer.writerow(row)
    except Exception as e:
        print(f"Error compiling CSV report {filename}: {str(e)}")
            
def generate_filter_report(file_name: str, filter_dict: dict) -> None:
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(file)
        writer.writerow(['donor_id', 'donation_id', 'appointment_date'])
        
        for donor_id, records in filter.items():
            for donation_id, appointment_date in records:
                writer.writerow([donor_id, donation_id, appointment_date])
                
def generate_ebv_report(file_name: str, donors: List[Donor]) -> None:
    headers = ['Donor ID', 'IDS Expiry', 'EBV IgG', 'EBV Testing Date', 'Donation Types', 'Age']
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            
            ebv_negative_donors = get_ebv_donors(donors)
            
            for donor in ebv_negative_donors:
                # print(f"GENERATE_EBV_REPORT IN REPORT.PY {donor}")
                donor_id = donor.donor_id
                ids_expiry = donor.last_ids_expiry.strftime('%m/%d/%Y') if isinstance(donor.last_ids_expiry, datetime) else str(donor.last_ids_expiry or 'N/A')
                ebv_igg_val = donor.ebv_igg
                ebv_igg_str = ebv_igg_val.strip().lower()
                ebv_testing_date = donor.ebv_testing_date.strftime('%m/%d/%Y')
                donation_types = ", ".join(donor.donation_types)
                row = {
                    'Donor ID': donor_id,
                    'IDS Expiry': ids_expiry,
                    # 'EBV Tested': 'Y' if donor.ebv_tested == True else 'N',
                    # 'EBV Negative': 'Y' if donor.ebv_negative == True else 'N',
                    'EBV IgG': ebv_igg_str,
                    'EBV Testing Date': ebv_testing_date,
                    'Donation Types': donation_types,
                    'Age': donor.age
                }
                
                writer.writerow(row)

        print(f"Exported: {file_name})")
    except Exception as err:
        print(f"Failed to generate report {file_name}: {err}")
          

