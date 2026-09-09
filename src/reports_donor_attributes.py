from datetime import datetime, date
from pathlib import Path

from src.config import load_config_data
from src.io_utils import load_donors
from src.report import generate_ebv_report


def get_ebv_report() -> None:
    config = load_config_data()
    
    print('\nLoading donor dataset....')
    donors = load_donors(config)
    
    print('\n' + '='*50)
    print("           EBV NEGATIVE REPORT GENERATION")
    print('='*50)
    
    base_dir = Path(config.get('output_dir', 'reports'))
    out_dir = base_dir / 'filtered_attributes'
    out_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%B-%d_%H%M')
    filename = out_dir / f"{timestamp}_ebv_neg_donors.csv"
    generate_ebv_report(filename, donors)
    
    