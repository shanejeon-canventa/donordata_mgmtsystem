from datetime import datetime, date
from pathlib import Path

from src.config import load_config_data
from src.io_utils import load_pipeline_dataset
from src.processing import group_appointments_by_donor, attach_appointments_to_donors, categorize_donor_appointments
from src.calculator import calculate_reliability_score
from src.screening import process_donor_recall, process_deep_screen, sort_donors_by_cell_lines
from src.models import RecallStatus
from src.report import generate_cell_line_csv_report


def run_cell_line_report_pipeline() -> None:
    """Runs the cell line cohort report generation workflow."""
    print("\n" + "="*50)
    print("      CELL LINE COHORT REPORT PIPELINE")
    print("="*50)

    config = load_config_data()
    today = date.today()

    print("\nLoading dataset files...")
    donors, appointments = load_pipeline_dataset(config)
    
    if not donors:
        print("Pipeline aborted: empty donor dataset.")
        return

    # Link appointments to donors
    grouped_appts = group_appointments_by_donor(appointments)
    attach_appointments_to_donors(donors, grouped_appts)

    # Calculate attendance reliability scores
    weights = config.get('scoring_weights', {})
    for donor in donors:
        categorize_donor_appointments(donor, today)
        print(donor.sorted_appointments)
        donor.reliability_score = calculate_reliability_score(donor.donor_id, donor.sorted_appointments, weights)
        # print(donor.reliability_score)

    # Evaluate recall & screening qualification
    process_donor_recall(donors)
    process_deep_screen(donors, config['deep_screen_criteria'])

    recallable = sum(1 for d in donors if d.recallability_status in (RecallStatus.RECALLABLE, RecallStatus.RECALLABLE_NEED_RESCREEN))
    deep_screened = sum(1 for d in donors if d.deep_screen)

    print(f"\nTotal Donors: {len(donors)} | Recallable: {recallable} | Deep Screen Eligible: {deep_screened}")

    # Generate output CSVs
    cohorts = sort_donors_by_cell_lines(donors, config['cell_line_ethnicity_map'])
    
    base_dir = Path(config.get('output_dir', 'reports'))
    out_dir = base_dir / "iPSC"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%B-%d_%H%M')

    print("\nGenerating CSV reports...")
    for idx, cohort_list in enumerate(cohorts, start=1):
        filename = out_dir / f"{timestamp}_cell_line_{idx}.csv"
        generate_cell_line_csv_report(str(filename), cohort_list)

    print("\nPipeline execution completed successfully.")