# Data transformations & appointment grouping
from datetime import date
from typing import List, Dict
from src.models import Donor, Appointment


def group_appointments_by_donor(appointments: List[Appointment]) -> Dict[str, List[Appointment]]:
    """Groups flat list of appointments into a donor-keyed lookup dictionary."""
    grouped: Dict[str, List[Appointment]] = {}
    for appt in appointments:
        grouped.setdefault(appt.donor_id, []).append(appt)
    return grouped


def attach_appointments_to_donors(donors: List[Donor], appt_map: Dict[str, List[Appointment]]) -> None:
    """Mutates donor objects in place by attaching mapped appointment lists."""
    for donor in donors:
        if donor.donor_id in appt_map:
            donor.appointments.extend(appt_map[donor.donor_id])


def categorize_donor_appointments(donor: Donor, evaluation_date: date) -> Dict[str, List[str]]:
    """Sorts donor appointments into status buckets relative to an evaluation date.
    
    Bucket choices: passed, failed, cancelled, no_show, pending, future.
    """
    categorized = {
        'passed': [],
        'failed': [],
        'cancelled': [],
        'no_show': [],
        'pending': [],
        'future': []
    }

    eval_date_only = evaluation_date.date() if hasattr(evaluation_date, 'date') else evaluation_date

    for appt in donor.appointments:
        appt_date_only = appt.appointment_date.date() if hasattr(appt.appointment_date, 'date') else appt.appointment_date
        is_future = appt_date_only >= eval_date_only
        
        details = f"{appt.appointment_date} {appt.appointment_time} | {appt.donation_id}"
        status = appt.donation_status.lower().strip()

        if status == 'passed':
            categorized['passed'].append(details)
        elif status == 'failed':
            categorized['failed'].append(details)
        elif status == 'cancelled by donor':
            categorized['cancelled'].append(details)
        elif status == 'no show':
            categorized['no_show'].append(details)
        elif status == 'pending':
            if not is_future:
                categorized['pending'].append(details)
            else:
                categorized['future'].append(details)

    # Sort historical buckets chronologically in descending order
    for bucket in categorized.values():
        bucket.sort(reverse=True)

    donor.sorted_appointments[donor.donor_id] = categorized
    return categorized
