from datetime import datetime
from pathlib import Path
from typing import List

from src.config import load_config_data
from src.io_utils import parse_donation_data, parse_appointment_data, load_appointment_merger
from src.report import generate_final_appointment_report, generate_filter_report

# def conslidated_manual_audit_report(merged_data: List[dict]) -> None:
#     merge_appointment_data()
def merge_appointment_data(appointment_data: List[dict], donation_data: List[dict]) -> List[dict]:
    """Cross references and extracts relevant data from appointments and donations to produce final appointment report data.

    Args:
        appointment_data (List[dict]): List of appointment data dictionaries
        donation_data (List[dict]): List of donation data dictionaries

    Returns:
        List[dict]: A list containing all cross-referenced donations and appointments.
    """
    
    config = load_config_data()
    donors, appointments = load_appointment_merger(config)
    donation_status_lookup = {
        donation['donation_id']: donation['donation_status']
        for donation in donation_data
    }
    
    missing_matches = 0
    final_appt_report = []
    
    for appointment in appointment_data:
        donation_id = appointment.get('donation_id')
        status = donation_status_lookup.get(donation_id, 'No Matching Donation')
        
        if status == 'No Matching Donation':
            missing_matches += 1
            print(f'missing match: {appointment}')
            continue
        
        report_row = appointment.copy()
        report_row['donation_status'] = status
        
        final_appt_report.append(report_row)
    
    print(f'missing matches: {missing_matches}')
    return final_appt_report


    # load donation data
    # load appt data
    # load consolidated data
    # print what needs review