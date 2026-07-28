import sys
from src.reports_cell_lines import run_cell_line_report_pipeline
from src.reports_scheduled_donors import test_scheduled_donors



def display_menu() -> None:
    """Renders main CLI selection prompts."""
    print("\n" + "="*45)
    print("      DONOR DATA MANAGEMENT PLATFORM")
    print("="*45)
    print(" Select a program to run:")
    print(" [1] Generate Cell Line Cohort Reports")
    print(" [2] Generate Demographics Summary (Coming Soon)")
    print(" [3] Generate Allergy & Medical Report (Coming Soon)")
    print(" [4] Test Script")
    print(" [Q] Quit Program")
    print("="*45)


def main() -> None:
    while True:
        display_menu()
        choice = input("\nEnter selection (1-4 or Q): ").strip().lower()

        if choice == '1':
            run_cell_line_report_pipeline()
        elif choice == '2':
            print("\nDemographics report module is currently in development.")
        elif choice == '3':
            print("\nAllergy & medical history module is currently in development.")
        elif choice == '4':
            test_scheduled_donors()
        elif choice in ('q', 'quit', 'exit'):
            print("\nExiting. Goodbye!\n")
            sys.exit()
        else:
            print("\nInvalid choice. Please pick an option from the menu.")

        input("\nPress ENTER to return to main menu...")


if __name__ == "__main__":
    main()