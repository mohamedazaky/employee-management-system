from employee_functions import *

MENU = {
    '1': ("Add Employee", add_employee_flow),
    '2': ("Display All Employees", display_all_employees),
    '3': ("Search by ID", search_by_id),
    '4': ("Search by Name", search_by_name),
    '5': ("Search by Department", search_by_department),
    '6': ("Search by Type", search_by_type),
    '7': ("Update Employee", update_employee),
    '8': ("Delete Employee", delete_employee),
    '9': ("Add Bonus", bonus_employee),
    '10': ("Add Deduction", deduction_employee),
    '11': ("Record Attendance", record_attendance),
    '12': ("Display Salary Details", display_salary_details),
    '13': ("Payroll Report", payroll_report),
    '14': ("Statistics", display_statistics),
}


def exit_program(emp_list):
    print("Saving employee data...")
    save_data(emp_list)
    print("Employee data saved successfully.")
    print("Thank you for using the Employee Management System.")
    print("Goodbye!")


def main():
    emp_list = load_data()

    try:
        while True:
            print("\n========================================")
            print("EMPLOYEE MANAGEMENT SYSTEM")
            print("========================================")
            for key, (label, _) in MENU.items():
                print(f"{key}. {label}")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == '0':
                exit_program(emp_list)
                break
            elif choice == '1':
                # add_employee_flow returns the updated list
                emp_list = add_employee_flow(emp_list)
            elif choice in MENU:
                MENU[choice][1](emp_list)
            else:
                print("Invalid menu option. Please try again.")
    except (KeyboardInterrupt, EOFError):
        print()
        exit_program(emp_list)


if __name__ == "__main__":
    main()
