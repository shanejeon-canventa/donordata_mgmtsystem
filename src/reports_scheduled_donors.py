from datetime import datetime, date

from src.config import load_config_data
from src.io_utils import load_pipeline_dataset
from src.processing import group_appointments_by_donor, attach_appointments_to_donors, categorize_donor_appointments
from src.screening import filter_donors_by_schedule_date

def test_scheduled_donors():
    config = load_config_data()
    today = date.today()
    
    print("\nLoading dataset files...")
    donors, appointments = load_pipeline_dataset(config)
    
    grouped_appts = group_appointments_by_donor(appointments)
    attach_appointments_to_donors(donors, grouped_appts)
    
    for donor in donors:
        categorize_donor_appointments(donor, today)
        
    filter_donors_by_schedule_date(donors, today)
    print(f"TODAY: {today} is {type(today)}")
    
