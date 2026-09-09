# import re
# from typing import List
# from src.models import Donor, RecallStatus
# from src.screening import process_donor_recall

# from datetime import datetime, date
# from pathlib import Path

# from src.config import load_config_data
# from src.io_utils import load_donors

# # clean up notes:
# # get part of notes that only contains "allergies"
# def extract_allergies_from_notes(donor: Donor):
#     donor_id = donor.donor_id
#     notes = donor.notes

#     pattern = r"[\"']|/lv"
#     CLEANUP_PATTERN = re.compile(pattern)
    
#     if notes != '':
#         segment = notes.split(';')
#         print(f'Donor {donor_id} notes: {segment}')
        
#     # if 'aller' in 

# def create_donor_allergy_lists(donors: List[Donor]) -> List:
#     allergies = []
#     no_allergies = []
    
#     process_donor_recall(donors)
#     for donor in donors:
#         recallable = donor.recallability_status
        
#         if recallable == RecallStatus.RECALLABLE or recallable == RecallStatus.RECALLABLE_NEED_RESCREEN:
#             if has_allergies:
#                 allergies.append(donor)
#             else:
#                 no_allergies.append(donor)
    
#     print(f'Recallable donors with allergies: {len(allergies)}')
#     print(f"\nRecallable donors without allergies {len(no_allergies)}")   
             
#     return [allergies, no_allergies]

# def generate_allergy_report(file_name: str, donors: List[Donor]) -> None:
#     allergy_headers = ['Donor ID', 'IDS Expiry', 'Recall Until', 'Has Allergies?', "Allergy Category", "Allergy"]
#     no_allergy_headers = ['Donor ID', 'IDS Expiry', "Recall Until" 'Has Allergies?']
#     try:
#         with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=allergy_headers)
#             writer.writeheader()
            
#             writer2 = csv.DictWriter(csv_file, fieldnames=no_allergy_headers)
#             writer2.writeheader()
            
#             donors_allergies, donors_no_allergies = create_donor_allergy_lists(donors)
            
#             for donor in donors_allergies:
#                 donor_id = donor.donor_id
#                 has_allergies = donor.has_allergies
#                 allergy_category = donor.allergies
#                 ids_expiry = donor.last_ids_expiry
#                 allergy = extract_allergies_from_notes(donor.notes)
                
            
            
            
            
# def test_allergy_code() -> None:
#     config = load_config_data()
    
#     print('\nLoading donor dataset...')
#     donors = load_donors(config)
    
#     create_donor_allergy_lists(donors)
    
    # print('\n' + '='*50)
    # print("          ALLERGY REPORT GENERATING")
    # print('='*50)
    
    # base_dir = Path(config.get('output_dir', 'reports'))
    # out_dir = base_dir / 'allergies'
    # out_dir.mkdir(parents=True, exist_ok=True)
# relevant data for allergy filter:
# filter donors for recall status, use process_donor_recall
# donor id, has_allergies, allergy_cateegory, notes, ids expiry, recallstatus
# get donors with self-reported allergies, append to list 'donors_with_allergies'
# else if, add to donors without allergies
# return 2 lists

# list comprehension to separate 


# create file from allergy list
# create file from no allergy list