from employee_functions import *

emp_list = load_data()

while True:
    print("\n========================================")
    print("EMPLOYEE MANAGEMENT SYSTEM")
    print("========================================")
    print("1. Add Employee")
    print("2. Display All Employees")
    print("3. Search by ID")
    print("4. Search by Name")
    print("5. Search by Department")
    print("6. Search by Type")
    print("7. Update Employee")
    print("8. Delete Employee")
    print("9. Add Bonus")
    print("10. Add Deduction")
    print("11. Record Attendance")
    print("12. Display Salary Details")
    print("13. Payroll Report")
    print("14. Statistics")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == '1':
        emp_list = add_employee_flow(emp_list)
    elif choice == '2':
        display_all_employees(emp_list)
    elif choice == '3':
        search_by_id(emp_list)
    elif choice == '4':
        search_by_name(emp_list)
    elif choice == '5':
        search_by_department(emp_list)
    elif choice == '6':
        search_by_type(emp_list)
    elif choice == '7':
        update_employee(emp_list)
    elif choice == '8':
        delete_employee(emp_list)
    elif choice == '9':
        bonus_employee(emp_list)
    elif choice == '10':
        deduction_employee(emp_list)
    elif choice == '11':
        recored_attendance(emp_list)
    elif choice == '12':
        display_salary_details(emp_list)
    elif choice == '13':
        payroll_report(emp_list)
    elif choice == '14':
        display_statistics(emp_list)
    elif choice == '0':
        print("Saving employee data...")
        save_data(emp_list)
        print("Employee data saved successfully.")
        print("Thank you for using the Employee Management System.")
        print("Goodbye!")
        break
    else:
        print("Invalid menu option. Please try again.")