import json
import os

# The data file always lives next to this script, no matter where the app is started from
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employee_data.json")

EMPLOYEE_TYPES = ["Full_Time", "Part_Time", "Freelancer"]

# Deduction rules for full-time employees (EGP)
ABSENCE_DEDUCTION = 200
LATE_DEDUCTION = 50

# The field that holds the pay rate for each employee type
RATE_FIELD = {
    "Full_Time": "basic_salary",
    "Part_Time": "hourly_rate",
    "Freelancer": "project_rate",
}


# ========================================
# Input helpers (console only)
# ========================================

def get_int(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")
            continue
        if min_value is not None and value < min_value:
            print(f"Please enter a number greater than or equal to {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Please enter a number less than or equal to {max_value}.")
            continue
        return value


def get_float(prompt, min_value=None):
    while True:
        try:
            value = float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")
            continue
        if min_value is not None and value < min_value:
            print(f"Please enter a number greater than or equal to {min_value}.")
            continue
        return value


def format_department(department):
    # Short names become acronyms (hr -> HR, it -> IT), longer ones get title case (finance -> Finance)
    department = department.strip()
    return department.upper() if len(department) <= 3 else department.title()


def ask_yes_no(prompt):
    return input(prompt).strip().lower() == 'y'


# ========================================
# Core logic (used by both the console and the web UI)
# ========================================

def is_id_exists(emp_list, new_id):
    for emp in emp_list:
        if emp["id"] == new_id:
            return True
    return False


def find_employee(emp_list, emp_id):
    for emp in emp_list:
        if emp["id"] == emp_id:
            return emp
    return None


def next_employee_id(emp_list):
    if len(emp_list) == 0:
        return 1
    return max(emp["id"] for emp in emp_list) + 1


def reset_type_fields(employee_info, employee_type, rate):
    # Remove the old type-specific fields, then add the fields for the new type
    for field in ["basic_salary", "absent_days", "late_days",
                  "hourly_rate", "working_hours",
                  "project_rate", "completed_projects"]:
        employee_info.pop(field, None)

    employee_info["employee_type"] = employee_type
    if employee_type == "Full_Time":
        employee_info["basic_salary"] = rate
        employee_info["absent_days"] = 0
        employee_info["late_days"] = 0
    elif employee_type == "Part_Time":
        employee_info["hourly_rate"] = rate
        employee_info["working_hours"] = 0
    elif employee_type == "Freelancer":
        employee_info["project_rate"] = rate
        employee_info["completed_projects"] = 0


def add_employee(emp_list, employee_id, name, age, department, employee_type, contact_info, salary):
    if is_id_exists(emp_list, employee_id):
        print("Error: Employee ID already exists")
        return emp_list

    if employee_type not in EMPLOYEE_TYPES:
        print("Error: Invalid employee type")
        return emp_list

    employee_info = {
        "id": employee_id,
        "name": name,
        "age": age,
        "department": department,
        "employee_type": employee_type,
        "contact_info": contact_info,
        "bonus": 0,
        "deduction": 0,
    }
    reset_type_fields(employee_info, employee_type, salary)

    emp_list.append(employee_info)
    return emp_list


def delete_employee_by_id(emp_list, emp_id):
    emp = find_employee(emp_list, emp_id)
    if emp is None:
        return False
    emp_list.remove(emp)
    return True


def add_bonus(emp, amount):
    emp["bonus"] += amount


def add_deduction(emp, amount):
    emp["deduction"] += amount


def get_rate(emp):
    return emp.get(RATE_FIELD.get(emp["employee_type"], ""), 0)


# ========================================
# Search
# ========================================

def filter_employees(emp_list, name="", department="", employee_type=""):
    results = []
    for emp in emp_list:
        if name and name.strip().lower() not in emp["name"].lower():
            continue
        if department and emp["department"].strip().lower() != department.strip().lower():
            continue
        if employee_type and emp["employee_type"] != employee_type:
            continue
        results.append(emp)
    return results


def print_employee_line(emp):
    print(f"ID: {emp['id']} | Name: {emp['name']} | Age: {emp['age']} | "
          f"Department: {emp['department']} | Type: {emp['employee_type']} | Contact: {emp['contact_info']}")


# ========================================
# Salary
# ========================================

def calculate_full_time_salary(emp_full_time):
    absence_deduction = emp_full_time["absent_days"] * ABSENCE_DEDUCTION
    late_deduction = emp_full_time["late_days"] * LATE_DEDUCTION
    final_salary = (emp_full_time["basic_salary"] + emp_full_time["bonus"]
                    - emp_full_time["deduction"] - absence_deduction - late_deduction)
    return final_salary


def calculate_part_time_salary(emp_part_time):
    salary = emp_part_time["hourly_rate"] * emp_part_time["working_hours"]
    return salary + emp_part_time["bonus"] - emp_part_time["deduction"]


def calculate_freelancer_salary(emp_freelancer):
    salary = emp_freelancer["project_rate"] * emp_freelancer["completed_projects"]
    return salary + emp_freelancer["bonus"] - emp_freelancer["deduction"]


def calculate_employee_salary(emp):
    if emp["employee_type"] == "Full_Time":
        return calculate_full_time_salary(emp)
    elif emp["employee_type"] == "Part_Time":
        return calculate_part_time_salary(emp)
    elif emp["employee_type"] == "Freelancer":
        return calculate_freelancer_salary(emp)
    return 0


def calculate_total_payroll(emp_list):
    total = 0
    for emp in emp_list:
        total += calculate_employee_salary(emp)
    return total


def calculate_average_salary(emp_list):
    if len(emp_list) == 0:
        return 0
    return calculate_total_payroll(emp_list) / len(emp_list)


def find_highest_paid_employee(emp_list):
    if len(emp_list) == 0:
        return None
    return max(emp_list, key=calculate_employee_salary)


def find_lowest_paid_employee(emp_list):
    if len(emp_list) == 0:
        return None
    return min(emp_list, key=calculate_employee_salary)


def get_statistics(emp_list):
    type_counts = {emp_type: 0 for emp_type in EMPLOYEE_TYPES}
    departments = {}
    for emp in emp_list:
        if emp["employee_type"] in type_counts:
            type_counts[emp["employee_type"]] += 1
        dept = emp["department"]
        departments[dept] = departments.get(dept, 0) + 1

    return {
        "total_employees": len(emp_list),
        "type_counts": type_counts,
        "departments": departments,
        "total_payroll": calculate_total_payroll(emp_list),
        "average_salary": calculate_average_salary(emp_list),
    }


# ========================================
# File handling
# ========================================

def save_data(emp_list):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(emp_list, file, indent=4, ensure_ascii=False)


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print("Employee file has an unexpected format. Starting with an empty list.")
                return []
            return data
    except FileNotFoundError:
        print("Employee file not found. A new employee database will be created.")
        return []
    except json.decoder.JSONDecodeError:
        print("Error while loading employee data.")
        print("Please check the employee file.")
        return []


# ========================================
# Console flows (menu options)
# ========================================

def choose_employee_type():
    while True:
        print("Select Employee Type (1, 2, 3):\n"
              "1. Full_Time\n"
              "2. Part_Time\n"
              "3. Freelancer")
        choice = input("--> ").strip()
        if choice in ['1', '2', '3']:
            return EMPLOYEE_TYPES[int(choice) - 1]
        print("Invalid employee type, try again.")


def ask_rate(employee_type):
    labels = {
        "Full_Time": "Enter the Basic Salary: ",
        "Part_Time": "Enter the Hourly Rate: ",
        "Freelancer": "Enter the Project Rate: ",
    }
    return get_float(labels[employee_type], min_value=0)


def ask_existing_employee(emp_list, prompt):
    # Keeps asking until an existing employee is found, or returns None if the user gives up
    while True:
        emp = find_employee(emp_list, get_int(prompt))
        if emp is not None:
            return emp
        print("Employee not found.")
        if not ask_yes_no("Search again? (y/n): "):
            return None


def add_employee_flow(emp_list):
    while True:
        while True:
            emp_id = get_int("Enter Employee ID: ", min_value=1)
            if is_id_exists(emp_list, emp_id):
                print("Error: Employee ID already exists")
                continue
            break

        name = input("Enter Employee Name: ").strip().title()
        age = get_int("Enter Employee Age: ", min_value=16, max_value=80)
        department = format_department(input("Enter Employee Department: "))
        contact = input("Enter Contact Info: ").strip()
        emp_type = choose_employee_type()
        salary = ask_rate(emp_type)

        emp_list = add_employee(emp_list, emp_id, name, age, department, emp_type, contact, salary)
        save_data(emp_list)
        print("Employee added successfully.")

        if not ask_yes_no("Do you want to add another employee? (y/n): "):
            return emp_list


def display_all_employees(emp_list):
    if len(emp_list) == 0:
        print("No employees to display.")
        return

    print("========================================\n"
          "ALL EMPLOYEES\n"
          "========================================")
    print(f"{'ID':<6}{'Name':<15}{'Type':<14}{'Department':<14}")
    print("-" * 49)
    for emp in emp_list:
        print(f"{emp['id']:<6}{emp['name']:<15}{emp['employee_type']:<14}{emp['department']:<14}")
    print("-" * 49)
    print(f"Total Employees: {len(emp_list)}")


def search_by_id(emp_list):
    emp = ask_existing_employee(emp_list, "Enter the ID: ")
    if emp is not None:
        print_employee_line(emp)


def run_search(emp_list, prompt, make_filter):
    while True:
        text = input(prompt).strip()
        results = make_filter(text)
        if results:
            for emp in results:
                print_employee_line(emp)
            return
        print(f"No employees found for: {text}")
        if not ask_yes_no("Search again? (y/n): "):
            return


def search_by_name(emp_list):
    run_search(emp_list, "Enter the Name: ",
               lambda text: filter_employees(emp_list, name=text))


def search_by_department(emp_list):
    run_search(emp_list, "Enter department: ",
               lambda text: filter_employees(emp_list, department=text))


def search_by_type(emp_list):
    def by_type(text):
        for emp_type in EMPLOYEE_TYPES:
            if emp_type.lower() == text.lower().replace("-", "_").replace(" ", "_"):
                return filter_employees(emp_list, employee_type=emp_type)
        return []

    run_search(emp_list, "Enter the employee type (Full_Time / Part_Time / Freelancer): ", by_type)


def update_employee(emp_list):
    while True:
        emp = ask_existing_employee(emp_list, "Enter the ID of the employee to update: ")
        if emp is None:
            break

        while True:
            print("What do you want to update?\n"
                  "1. Name\n"
                  "2. ID\n"
                  "3. Age\n"
                  "4. Department\n"
                  "5. Employee type\n"
                  "6. Contact\n"
                  "7. Pay rate\n"
                  "or type 'done' to finish")
            choice = input("Choice number: ").strip().lower()

            if choice == "done":
                print("Done editing this employee.")
                break
            elif choice == '1':
                emp['name'] = input("Enter the new Name: ").strip().title()
            elif choice == '2':
                new_id = get_int("Enter the new ID: ", min_value=1)
                if new_id != emp['id'] and is_id_exists(emp_list, new_id):
                    print("Error: Employee ID already exists")
                    continue
                emp['id'] = new_id
            elif choice == '3':
                emp['age'] = get_int("Enter the new Age: ", min_value=16, max_value=80)
            elif choice == '4':
                emp['department'] = format_department(input("Enter the new Department: "))
            elif choice == '5':
                new_type = choose_employee_type()
                if new_type != emp['employee_type']:
                    reset_type_fields(emp, new_type, ask_rate(new_type))
            elif choice == '6':
                emp['contact_info'] = input("Enter the new contact info: ").strip()
            elif choice == '7':
                emp[RATE_FIELD[emp['employee_type']]] = ask_rate(emp['employee_type'])
            else:
                print("Invalid choice, try again.")
                continue

            save_data(emp_list)
            print("Employee updated successfully.")
            print_employee_line(emp)

            if not ask_yes_no("Update another field for this employee? (y/n): "):
                break

        if not ask_yes_no("Update another employee? (y/n): "):
            break
    save_data(emp_list)


def delete_employee(emp_list):
    while True:
        emp = ask_existing_employee(emp_list, "Enter the ID for deleting: ")
        if emp is None:
            break

        print_employee_line(emp)
        if ask_yes_no("Delete this employee? (y/n): "):
            emp_list.remove(emp)
            save_data(emp_list)
            print("Employee deleted successfully.")
        else:
            print("Cancelled, employee not deleted.")

        if not ask_yes_no("Do you want to delete another employee? (y/n): "):
            break


def bonus_employee(emp_list):
    while True:
        emp = ask_existing_employee(emp_list, "Enter the ID of the employee to add a bonus: ")
        if emp is None:
            break

        amount = get_float("Enter the bonus: ", min_value=0)
        old_bonus = emp["bonus"]
        add_bonus(emp, amount)
        save_data(emp_list)
        print(f"Current bonus = {old_bonus}\n"
              f"New bonus entered = {amount}\n"
              f"Total bonus = {emp['bonus']}")

        if not ask_yes_no("Add a bonus for another employee? (y/n): "):
            break


def deduction_employee(emp_list):
    while True:
        emp = ask_existing_employee(emp_list, "Enter the ID of the employee to add a deduction: ")
        if emp is None:
            break

        amount = get_float("Enter the amount of deduction: ", min_value=0)
        old_deduction = emp["deduction"]
        add_deduction(emp, amount)
        save_data(emp_list)
        print(f"Current deduction = {old_deduction}\n"
              f"New deduction entered = {amount}\n"
              f"Total deduction = {emp['deduction']}")

        if not ask_yes_no("Add a deduction for another employee? (y/n): "):
            break


def record_attendance(emp_list):
    while True:
        emp = ask_existing_employee(emp_list, "Enter the ID of the employee to record attendance: ")
        if emp is None:
            break

        if emp['employee_type'] == 'Full_Time':
            choice = input("Select (1 | 2):\n"
                           "1. Absent day\n"
                           "2. Late day\n"
                           "--> ").strip()
            if choice == '1':
                emp["absent_days"] += 1
                print(f"Attendance recorded successfully!\nTotal absent days: {emp['absent_days']}")
            elif choice == '2':
                emp["late_days"] += 1
                print(f"Attendance recorded successfully!\nTotal late days: {emp['late_days']}")
            else:
                print("Invalid choice, nothing recorded.")

        elif emp["employee_type"] == "Part_Time":
            hours = get_int("Enter the number of hours: ", min_value=1)
            emp["working_hours"] += hours
            print(f"Attendance recorded successfully!\nTotal working hours: {emp['working_hours']}")

        elif emp["employee_type"] == "Freelancer":
            emp["completed_projects"] += 1
            print(f"Project recorded successfully!\nTotal completed projects: {emp['completed_projects']}")

        save_data(emp_list)
        if not ask_yes_no("Record attendance for another employee? (y/n): "):
            break


def display_salary_details(emp_list):
    while True:
        emp = ask_existing_employee(emp_list, "Enter the ID of the employee to display salary details: ")
        if emp is None:
            break

        print("========================================\n"
              "SALARY DETAILS\n"
              "========================================\n"
              f"Employee: {emp['name']}\n"
              f"Employee Type: {emp['employee_type']}\n")

        if emp['employee_type'] == 'Full_Time':
            print(f"Basic Salary: {emp['basic_salary']}\n"
                  f"Bonus: {emp['bonus']}\n"
                  f"Deduction: {emp['deduction']}\n"
                  f"Absent Days: {emp['absent_days']}\n"
                  f"Absence Deduction: {emp['absent_days'] * ABSENCE_DEDUCTION}\n"
                  f"Late Days: {emp['late_days']}\n"
                  f"Late Deduction: {emp['late_days'] * LATE_DEDUCTION}")
        elif emp['employee_type'] == 'Part_Time':
            print(f"Hourly Rate: {emp['hourly_rate']}\n"
                  f"Working Hours: {emp['working_hours']}\n"
                  f"Bonus: {emp['bonus']}\n"
                  f"Deduction: {emp['deduction']}")
        elif emp['employee_type'] == 'Freelancer':
            print(f"Project Rate: {emp['project_rate']}\n"
                  f"Completed Projects: {emp['completed_projects']}\n"
                  f"Bonus: {emp['bonus']}\n"
                  f"Deduction: {emp['deduction']}")

        print("----------------------------------------\n"
              f"Final Salary: {calculate_employee_salary(emp):,.2f} EGP\n"
              "========================================")

        if not ask_yes_no("Display another salary? (y/n): "):
            break


def payroll_report(emp_list):
    if len(emp_list) == 0:
        print("No employees to display.")
        return

    print("========================================\n"
          "MONTHLY PAYROLL REPORT\n"
          "========================================")
    print(f"{'ID':<6}{'Name':<15}{'Type':<14}{'Final Salary':>14}")
    print("-" * 49)
    for emp in emp_list:
        print(f"{emp['id']:<6}{emp['name']:<15}{emp['employee_type']:<14}{calculate_employee_salary(emp):>14,.2f}")
    print("-" * 49)

    print(f"Total Payroll: {calculate_total_payroll(emp_list):,.2f} EGP")
    print(f"Average Salary: {calculate_average_salary(emp_list):,.2f} EGP")

    highest_paid = find_highest_paid_employee(emp_list)
    lowest_paid = find_lowest_paid_employee(emp_list)
    print(f"\nHighest Paid Employee:\n{highest_paid['name']} - {calculate_employee_salary(highest_paid):,.2f} EGP")
    print(f"\nLowest Paid Employee:\n{lowest_paid['name']} - {calculate_employee_salary(lowest_paid):,.2f} EGP")


def display_statistics(emp_list):
    if len(emp_list) == 0:
        print("No employees to display.")
        return

    stats = get_statistics(emp_list)
    print("========================================\n"
          "EMPLOYEE STATISTICS\n"
          "========================================\n")
    print(f"Total Employees: {stats['total_employees']}\n")
    print(f"Full-Time Employees: {stats['type_counts']['Full_Time']}")
    print(f"Part-Time Employees: {stats['type_counts']['Part_Time']}")
    print(f"Freelancers: {stats['type_counts']['Freelancer']}\n")
    for dept, count in stats['departments'].items():
        print(f"{dept} Department: {count}")
    print(f"\nTotal Payroll: {stats['total_payroll']:,.2f} EGP")
    print(f"Average Salary: {stats['average_salary']:,.2f} EGP")
