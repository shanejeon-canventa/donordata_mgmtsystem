# Business logic: Recall & Deep Screen eligibility
from typing import List, Tuple
from src.models import Donor
from datetime import datetime
# from src.utils import parse_date_string


def process_donor_recall(donor_data: List[Donor]) -> None:
    """Batch-evaluates recall eligibility for all loaded donors."""
    for donor in donor_data:
        donor.evaluate_recall()


def process_deep_screen(donor_data: List[Donor], criteria: dict) -> None:
    """Batch-evaluates deep screening suitability against configured rules."""
    for donor in donor_data:
        donor.evaluate_deep_screen_eligibility(criteria)


def sort_donors_by_cell_lines(donor_data: List[Donor], cohort_rules: dict) -> Tuple[List[Donor], ...]:
    """Splits deep-screen eligible donors into cohorts using configured ethnicity maps."""
    cohorts = {key: [] for key in cohort_rules.keys()}

    for donor in donor_data:
        if not donor.deep_screen:
            continue

        ethnicity = donor.ethnicity.strip().lower()
        sex = donor.sex.strip().lower()

        # Match donor against configured cohort parameters
        for cohort_key, rule in cohort_rules.items():
            ethnic_match = ethnicity in rule['ethnicities']
            gender_match = (sex == 'male') if rule.get('require_male') else True

            if ethnic_match and gender_match:
                cohorts[cohort_key].append(donor)
                break

    return tuple(cohorts.values())

def filter_donors_by_schedule_date(donors_list, target_date):
    matching_donors_summary = []
    
    for donor in donors_list:
        relevant_fields = {}
        donor_id = donor.donor_id
        future_appointments = donor.sorted_appointments[donor_id]['future']

        if len(future_appointments) > 1:
            print("Multiple future appointments found.")
            continue
        if len(future_appointments) == 1:
        
            appt_date_str = future_appointments[0].split(' | ')[0]
            appt_dt_obj = datetime.strptime(appt_date_str, '%Y-%m-%d %H:%M:%S').date()
            
            # print(f"appt date is on {appt_date}")
            print(f"APPT DATE {appt_dt_obj} is {type(appt_dt_obj)}")
            
            if appt_dt_obj == target_date:
                matching_donors_summary.append((donor_id, appt_date_str))
           
    print(f"TESTING: {matching_donors_summary}")            
    return matching_donors_summary
                                               
            
            
        
