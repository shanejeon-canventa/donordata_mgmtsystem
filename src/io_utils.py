# Pure CSV/File readers & parsing helpers
import csv
import re
from datetime import datetime
from typing import List, Optional, Tuple
from src.models import Donor, Appointment
from src.utils import _parse_csv_date, _parse_csv_bool, _parse_csv_float, _parse_csv_list, parse_date_string


def extract_date_from_notes(notes: Optional[str], anchor_date: Optional[datetime]) -> Optional[datetime]: #which notes?
    """Scans free-text notes for dates and imputes missing years from anchor dates."""
    if not notes or not anchor_date:
        return None
        
    pattern = r"(\d{1,2}/\d{1,2})(?:/(\d{4}))?"
    match = re.search(pattern, notes)
    
    if match:
        partial_date = match.group(1)
        explicit_year = match.group(2)
        year_to_use = explicit_year if explicit_year else str(anchor_date.year)
        
        try:
            return datetime.strptime(f"{partial_date}/{year_to_use}", '%m/%d/%Y')
        except ValueError:
            return None
            
    return None


def load_csv_dict_reader(csv_path: str, processing_function, *args):
    """Context wrapper for reading CSV records cleanly into memory."""
    with open(csv_path, mode='r', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        return processing_function(reader, *args)


def load_complete_donor_data(reader_data, *args) -> List[Donor]:
    """Parses raw CSV dict rows into initialized Donor data classes."""
    donors = []
    skipped_count = 0

    for row_number, row in enumerate(reader_data, start=1):
        raw_id = row.get('Donor ID', '').strip()
        parsed_dob = _parse_csv_date(row.get('Date of Birth', '').strip())

        # Gatekeeper: ensure ID exists and matches prefix conventions
        if not raw_id or not parsed_dob or not raw_id.lower().startswith('ce'):
            skipped_count += 1
            continue

        # Real-time age calculation taking birthday month/day into account
        today = datetime.now()
        real_age = today.year - parsed_dob.year - ((today.month, today.day) < (parsed_dob.month, parsed_dob.day))

        try:
            donor_obj = Donor(
                donor_id=raw_id,
                eligibility=row.get('Eligibility', 'unknown'),
                blood_type=row.get('Blood Type', 'unknown'),
                date_of_birth=parsed_dob,
                age=real_age,
                sex=row.get('Sex', 'unknown'),
                ethnicity=row.get('Ethnicity', 'unknown'),
                donation_types=_parse_csv_list(row.get('Donation Types', '')),
                weight_kg=_parse_csv_float(row.get('Weight (kg)')),
                weight_lb=_parse_csv_float(row.get('Weight (lbs)')),
                height_cm=_parse_csv_float(row.get('Height (cm)')),
                height_in=_parse_csv_float(row.get('Height (inches)')),
                bmi=_parse_csv_float(row.get('BMI')),
                taking_daily_meds=_parse_csv_bool(row.get('Taking Daily Meds')),
                tobacco_use=_parse_csv_bool(row.get('Tobacco Use')),
                has_allergies=_parse_csv_bool(row.get('Has Allergies?')),
                hla_testing_complete=_parse_csv_bool(row.get('HLA Testing Complete')),
                hla_a2_positive=_parse_csv_bool(row.get('HLA A2 Positive')),
                # ebv_tested=_parse_csv_bool(row.get('EBV tested')),
                # ebv_negative=_parse_csv_bool(row.get('EBV negative')),
                last_ids_screen=_parse_csv_date(row.get('Last IDS Screen')),
                last_ids_expiry=_parse_csv_date(row.get('Last IDS Expiry')),
                hemoglobin=_parse_csv_float(row.get('Hemoglobin')),
                platelet=_parse_csv_float(row.get('Platelet')),
                hematocrit=_parse_csv_float(row.get('Hematocrit')),
                pulse_rate=_parse_csv_float(row.get('Pulse Rate')),
                wbc=_parse_csv_float(row.get('WBC')),
                rbc=_parse_csv_float(row.get('RBC')),
                systolic=_parse_csv_float(row.get('Systolic')),
                diastolic=_parse_csv_float(row.get('Diastolic')),
                temperature=_parse_csv_float(row.get('Temperature')),
                within_90_day_ids_window=_parse_csv_bool(row.get('Within 90 Day IDS Window')),
                econsent_for_tax_documents=_parse_csv_bool(row.get('E-Consent for Tax documents')),
                bm_type=row.get('BM Type') or None,
                cmv_total_ab=_parse_csv_bool(row.get('CMV Total AB')) if row.get('CMV Total AB') else None,
                cmv_igg=row.get('CMV IgG', ''),
                ebv_igg=row.get('EBV IgG', ''),
                ebv_testing_date=_parse_csv_date(row.get('EBV Testing Date')),
                allergies=row.get('Allergies') or None,
                last_bm_donation=_parse_csv_date(row.get('Last BM Donation')),
                last_lp_donation=_parse_csv_date(row.get('Last LP Donation')),
                econsent_date=_parse_csv_date(row.get('e-Consent Date')),
                notes=row.get('Notes') or None,
                ebv_ab_profile_testing_date=_parse_csv_date(row.get('EBV Ab Profile testing date')),
                ebv_ab_profile=_parse_csv_bool(row.get('EBV Ab profile')) if row.get('EBV Ab profile') else None,
            )
            donors.append(donor_obj)
        except ValueError as err:
            print(f"Skipping row {row_number} (ID: {raw_id}) - Data error: {err}")

    if skipped_count > 0:
        print(f"Skipped {skipped_count} row(s) due to invalid donor ID formatting or birth dates.")
        
    return donors


def load_appointment_records(reader_data, excluded_ids: Optional[List[str]] = None) -> List[Appointment]:
    """Ingests appointment records while ignoring flagged exclusion IDs."""
    skip_set = set(excluded_ids or [])
    appointments = []

    for row in reader_data:
        donor_id = row.get('Donor ID', '').strip()
        donation_id = row.get('Donation ID', '').strip()

        if not donor_id or donor_id in skip_set or not donation_id:
            continue

        appt_date_str = row.get('Appointment Date', '').strip()
        appt_time_str = row.get('Appointment Time', '').strip()

        if not appt_date_str or not appt_time_str:
            continue

        try:
            appointments.append(Appointment(
                donor_id=donor_id,
                donation_id=donation_id,
                donation_type=row.get('Donation Type', '').strip(),
                appointment_date=datetime.strptime(appt_date_str, '%m/%d/%Y').date(),
                appointment_time=datetime.strptime(appt_time_str, '%H:%M%p').time(),
                appointment_status=row.get('Appointment Status', '').strip(),
                donation_status=row.get('Donation Status', '').strip()
            ))
        except Exception:
            # Skip invalid date/time formatting rows gracefully
            continue

    return appointments


def load_pipeline_dataset(config: dict) -> Tuple[List[Donor], List[Appointment]]:
    """Standardized entry point for loading CRM and appointment datasets across all modules."""
    donors = load_csv_dict_reader(config['donors'], load_complete_donor_data)
    excluded = config.get('excluded_donor_ids', [])
    appointments = load_csv_dict_reader(config['appointments_final'], load_appointment_records, excluded)
    
    return donors, appointments

def load_donors(config: dict) -> List[Donor]: 
    """Loads CRM donor data"""
    print(f"\nLOADING (ONLY) DONOR DATA")
    print('*'*20)
    donors = load_csv_dict_reader(config['donors'], load_complete_donor_data)
    return donors

# MERGING DONATIONS WITH APPOINTMENTS ---> PRODUCE APPOINTMENTS_FINAL.CSV

def parse_donation_data(config: dict) -> List[dict]:
    donations = []
    statuses = {}
    for row_number, row in enumerate(config, start=1):
        donor_id = row.get('Donor ID', '').strip()
        donation_id = row.get('Description', '').strip()
        donation_type = row.get('Type', '').strip()
        donation_status = row.get('Status', '').strip().lower()
        
        if donor_id == '':
            print(f"XXX Row: {row_number} has no donor ID found XXX")
            continue
        if donation_id == '':
            print(f"XXX Row: {row_number} has no donation ID found XXX")
            continue
        if donation_status not in statuses:
            statuses[donation_status] = 0
        elif donation_status in statuses:
            statuses[donation_status] += 1
            
        donation_dict = {'donor_id': donor_id, 'donation_id': donation_id, 'donation_type': donation_type, 'donation_status': donation_status}
        donations.append(donation_dict)
        
    return donations 

def parse_appointment_data(config: dict) -> List[dict]:
    appointments = []
    skipped = {'donor_id': 0, 'donation_id': 0, 'appointment_date': 0}
    
    for row_number, row in enumerate(reader_data, start=1):
        donor_id = row.get('Donor ID', '').strip()
        donation_id = row.get('About', '').strip()
        donation_type = row.get('Donation Type', '').strip()
        appointment_date_string = row.get('Date / Time', '').strip()
        appointment_subject = row.get('Subject', '').strip().lower()
        
        if donor_id == '':
            skipped['donor_id'] += 1
            continue
        if donation_id == '':
            skipped['donation_id'] += 1
            continue
        if appointment_date_string == '':
            skipped['appointment_date'] += 1
            continue
    
        appointment_date, appointment_time = parse_date_string(appointment_date_string)
        appointment_dict = {
            'donor_id': donor_id,
            'donation_id': donation_id,
            'donation_type': donation_type,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'appointment_status': appointment_status,
            'appointment_subject': appointment_subject
        }
        appointments.append(appointment_dict)
    
    print(f"Rows skipped: {skipped}")
    return appointments

def load_appointment_merger(config: dict) -> Tuple[List[Donor], List[Appointment]]:
    """Standardized entry point for loading donation and appointment datasets."""
    donations = load_csv_dict_reader(config['donations'], parse_donation_data)
    appointments = load_csv_dict_reader(config['appointments_raw'], parse_appointment_data)
    
    return donations, appointments