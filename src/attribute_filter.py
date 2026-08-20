from typing import List
from models import Donor

def get_ebv_donors(ebv_status: str, donors: Donor) -> List:
    """Compiles lists of donors based on EBV status

    Args:
        ebv_status (string): Boolean choice user makes to select ebv status type sought for generation
        donors (Donor): Donors to iterate through

    Returns:
        List: returns negative, positive, and unknown lists in comprehensive list
    """
    negative = []
    positive = []
    unknown = []
    
    for donor in donors:
        donor_id = donor.donor_id
        ebv = donor.ebv_igg.trim().lower()
        ids_expiry = donor.ids_expiry
        
        if ebv_status == 'negative' and ebv == 'negative' or ebv.startswith('neg'):
            negative.append((donor_id, ebv, ids_expiry))
        elif ebv_status == 'positive' and ebv == 'positive' or ebv.startswith('pos'):
            positive.append((donor_id, ebv, ids_expiry))
        else:
            unknown.append((donor_id, ebv, ids_expiry))
    
    return [negative, positive, unknown]



def get_cmv_donors(cmv_status: str, donors: Donor) -> List:
    """Compiles lists of donors based on cmv status

    Args:
        cmv_status (string): Boolean choice user makes to select cmv status type sought for generation
        donors (Donor): Donors to iterate through

    Returns:
        List: returns negative, positive, and unknown lists in comprehensive list
    """
    negative = []
    positive = []
    unknown = []
    
    for donor in donors:
        donor_id = donor.donor_id
        cmv = donor.cmv_igg.trim().lower()
        ids_expiry = donor.ids_expiry
        
        if cmv_status == 'negative' and cmv == 'negative' or cmv.startswith('neg'):
            negative.append((donor_id, cmv, ids_expiry))
        elif cmv_status == 'positive' and cmv == 'positive' or cmv.startswith('pos'):
            positive.append((donor_id, cmv, ids_expiry))
        else:
            unknown.append((donor_id, cmv, ids_expiry))
    
    return [negative, positive, unknown]
