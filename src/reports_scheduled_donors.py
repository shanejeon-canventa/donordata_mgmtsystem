from datetime import datetime, date
from pathlib import Path

from src.config import load_config_data
from src.io_utils import load_donors
from src.processing import group_appointments_by_donor, attach_appointments_to_donors, categorize_donor_appointments
from src.screening import process_donor_recall
from src.attribute_filter import get_ebv_donors
from src.report import generate_donor_demographics_csv_report

    
def get_donor_demographics_report() -> None:
    """Generates donor demographics report."""
    config = load_config_data()
    
    print('\nLoading donor dataset...')
    donors = load_donors(config)
    
    print('\n' + '='*50)
    print("           DEMOGRAPHICS REPORT GENERATION")
    print('='*50)
    
    base_dir = Path(config.get('output_dir', 'reports'))
    out_dir = base_dir / "demographics"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%B-%d_%H%M')
    filename = out_dir / f"{timestamp}_donor_demographics.csv"
    generate_donor_demographics_csv_report(str(filename), donors)
    
    print("\nDonor Demographics execution completed successfully.")
    
    