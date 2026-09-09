import sys
from src.reports_cell_lines import run_cell_line_report_pipeline
from src.reports_scheduled_donors import get_donor_demographics_report
from src.reports_donor_attributes import get_ebv_report
# from src.allergies import test_allergy_code



def display_menu() -> None:
    """Renders main CLI selection prompts."""
    # OPTIMIZE THIS
    print("\n" + "="*45)
    print("      DONOR DATA MANAGEMENT PLATFORM")
    print("="*45)
    print(" Select a program to run:")
    print(" [1] Generate iPSC Deep Screen Cell Line Reports")
    print(" [2] Generate Demographics Report")
    print(" [3] Generate Allergy & Medical Report (Coming Soon)")
    print(" [4] Reliable Donors (Coming Soon)")
    print(" [5] Consolidate Appointments and Donations")
    print(" [6] Generate Report Based on Donor Attribute")
    print(" [Q] Quit Program")
    print("="*45)

def display_sub_menu() -> None:
    """Renders attribute CLI prompts."""
    print("\n" + "="*45)
    print("      DONOR ATTRIBUTE SELECTION")
    print(" [A] EBV Negative")
    
def main() -> None:
    while True:
        display_menu()
        choice = input("\nEnter selection (1-6 or Q): ").strip().lower()

        if choice == '1':
            run_cell_line_report_pipeline()
        elif choice == '2':
            get_donor_demographics_report()
        elif choice == '3':
            print("\nAllergy module is currently in development.")
            # test_allergy_code()
        elif choice == '4':
            print("\nReliable donor report module is currently in development.")
        elif choice == '5':
            print("\n IN PROGRESS")
        elif choice == '6':
            display_sub_menu()
            attribute = input("\nSelect attribute ").upper()
            if attribute == 'A':
                get_ebv_report()
        elif choice in ('q', 'quit', 'exit'):
            print("\nALL DONE. BYE BYE!\n")
            sys.exit()
        else:
            print("\nInvalid choice. Please pick an option from the menu.")

        input("\nPress ENTER to return to main menu...")


if __name__ == "__main__":
    main()