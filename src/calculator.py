# Calculation algorithms
def calculate_reliability_score(donor_key: str, appt_history: dict, weights: dict) -> float:
    """Calculates attendance ratio (0.0 - 100.0) based on weighted appointment status scores."""
    appt_dict = appt_history.get(donor_key, {})

    passed = len(appt_dict.get('passed', []))
    failed = len(appt_dict.get('failed', []))
    cancelled = len(appt_dict.get('cancelled', []))
    no_show = len(appt_dict.get('no_show', []))

    total = passed + failed + cancelled + no_show
    if total == 0:
        return 0.0

    points = (
        (passed * weights.get('passed', 1.0)) +
        (failed * weights.get('failed', 0.75)) +
        (cancelled * weights.get('cancelled', 0.50)) +
        (no_show * weights.get('no_show', 0.0))
    )

    return round((points / total) * 100, 2)