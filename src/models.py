from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timedelta


class RecallStatus(Enum):
    UNEVALUATED = 0
    RECALLABLE = 1
    RECALLABLE_NEED_RESCREEN = 2
    NOT_RECALLABLE = 3
    DISQUALIFIED = 4


@dataclass
class Appointment:
    """Represents an individual scheduled or completed donation attempt."""
    donor_id: str
    donation_id: str
    donation_type: str
    appointment_date: datetime
    appointment_time: datetime
    appointment_status: str
    donation_status: str


@dataclass
class Donor:
    """Core domain model mapping CRM demographic profile and historical metrics."""
    donor_id: str
    eligibility: str
    blood_type: str
    date_of_birth: datetime
    age: int
    sex: str
    ethnicity: str
    donation_types: list

    weight_kg: float
    weight_lb: float
    height_cm: float
    height_in: float
    bmi: float

    taking_daily_meds: bool
    tobacco_use: bool
    has_allergies: bool
    hla_testing_complete: bool
    hla_a2_positive: bool
    
    # ebv_tested: bool
    # ebv_negative: bool

    last_ids_screen: Optional[datetime]
    last_ids_expiry: Optional[datetime]

    hemoglobin: float
    platelet: float
    hematocrit: float
    pulse_rate: float
    wbc: float
    rbc: float
    systolic: float
    diastolic: float
    temperature: float

    within_90_day_ids_window: bool
    econsent_for_tax_documents: bool

    # Relational & State Tracking
    appointments: List[Appointment] = field(default_factory=list)
    sorted_appointments: dict = field(default_factory=dict)
    recallability_status: RecallStatus = RecallStatus.UNEVALUATED
    deep_screen: bool = False
    reliability_score: Optional[float] = None
    ebv_neg_recall: bool = False

    # Optional Clinical Markers
    bm_type: Optional[str] = None
    cmv_total_ab: Optional[bool] = None
    cmv_igg: Optional[str] = None
    ebv_igg: Optional[str] = None
    ebv_testing_date: Optional[datetime] = None
    allergies: Optional[str] = None
    last_bm_donation: Optional[datetime] = None
    last_lp_donation: Optional[datetime] = None
    econsent_date: Optional[datetime] = None
    notes: Optional[str] = None
    ebv_ab_profile_testing_date: Optional[datetime] = None
    ebv_ab_profile: Optional[bool] = None
    ebv_testing_date: Optional[datetime] = None

    def _qualifies_for_lp(self) -> bool:
        """Quick check to verify if donor is cleared for Leukapheresis."""
        return any(d.strip().lower() == "lp" for d in self.donation_types)

    def evaluate_recall(self) -> None:
        """Determines recall eligibility using eligibility state and IDS expiration dates."""
        status = self.eligibility.lower().strip()
        today = datetime.now()

        # Handle missing expiration records safely
        days_overdue = 9999
        if self.last_ids_expiry:
            days_overdue = 0 if self.last_ids_expiry > today else (today - self.last_ids_expiry).days

        # Priority screening overrides
        if status in ('ineligible', 'deferred'):
            self.recallability_status = RecallStatus.DISQUALIFIED
        elif self.age > 55 or status == 'not responsive':
            self.recallability_status = RecallStatus.NOT_RECALLABLE
        elif status == 'eligible':
            self.recallability_status = RecallStatus.RECALLABLE
        elif status == 'ids expired' and days_overdue <= 90:
            self.recallability_status = RecallStatus.RECALLABLE_NEED_RESCREEN
        elif status == 'ids expired' and days_overdue > 90:
            self.recallability_status = RecallStatus.NOT_RECALLABLE

    def evaluate_deep_screen_eligibility(self, criteria: dict) -> None:
        """Evaluates whether donor meets parameters for iPSC deep screen inclusion."""
        is_recallable = self.recallability_status in (
            RecallStatus.RECALLABLE, 
            RecallStatus.RECALLABLE_NEED_RESCREEN
        )
        
        meets_age = criteria['min_age'] <= self.age <= criteria['max_age']
        meets_bmi = criteria['min_bmi'] <= self.bmi <= criteria['max_bmi']
        
        if is_recallable and self._qualifies_for_lp() and meets_age and meets_bmi and not self.tobacco_use:
            # Custom demographic exclusions 
            if criteria.get('exclude_female_caucasian'):
                if self.sex.strip().lower() == 'female' and self.ethnicity.strip().lower() == 'caucasian':
                    return
                    
            self.deep_screen = True
            
    def evaluate_ebv_negative_donors(self) -> None:
        is_recallable = self.recallability_status in (
            RecallStatus.RECALLABLE,
            RecallStatus.RECALLABLE_NEED_RESCREEN
        )
        
        if self.ebv_testing_date != None:
            today = datetime.now()
            ninety_days_ago = today - timedelta(days=90)
            print(f'EBV TESTING: {self.ebv_testing_date}')
            valid_labs = self.ebv_testing_date > ninety_days_ago
            
            if is_recallable and self._qualifies_for_lp() and self.ebv_igg.strip().lower().startswith('neg') and valid_labs == True:
                self.ebv_neg_recall = True
                print(f'donor ID: {self.donor_id}')
                