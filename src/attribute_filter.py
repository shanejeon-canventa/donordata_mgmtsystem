from typing import List
from src.models import Donor, RecallStatus
from src.screening import process_donor_recall, process_ebv_neg_donors

def get_ebv_donors(donors: Donor) -> List:
    """Compiles lists of NEGATIVE EBV donors

    Args:
        donors (Donor): Donors to iterate through

    Returns:
        List: returns list of Donors with EBV status NEGATIVE
    """
    negative = []
    
    process_donor_recall(donors)
    process_ebv_neg_donors(donors)
    
    for donor in donors:
        # ebv_igg = donor.ebv_igg
        if donor.ebv_neg_recall:
            negative.append(donor)
        
        # negative = [donor for donor in donors if donor.ebv_igg.startswith('neg') and donor.within_90_day_ids_window]
        # # return [negative, positive, unknown]
        # print(f'ALL EBV NEGATIVE DONORS {len(negative)}')
    # return 
    return negative



def get_cmv_donors(donors: Donor) -> List:
    """Compiles lists of donors based on cmv NEGATIVE

    Args:
        donors (Donor): Donors to iterate through

    Returns:
        List: returns negative, positive, and unknown lists in comprehensive list
    """
    negative = []
    # positive = []
    # unknown = []
    
    for donor in donors:
        donor_id = donor.donor_id
        cmv = donor.cmv_igg.strip().lower()
        ids_expiry = donor.ids_expiry
        
        if cmv == 'negative' or cmv.startswith('neg'):
            negative.append((donor_id, cmv, ids_expiry))
        # elif cmv_status == 'positive' and cmv == 'positive' or cmv.startswith('pos'):
        #     positive.append((donor_id, cmv, ids_expiry))
        # else:
        #     unknown.append((donor_id, cmv, ids_expiry))
    
    # return [negative, positive, unknown]
    return negative