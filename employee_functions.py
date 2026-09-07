import json

def is_id_exists(emp_list, new_id):
    found = False
    for emp in emp_list:
        if emp["id"] == new_id:
                found = True
    return found

def Add_Eployee(emp_list , Employee_ID , Name , Age , Department , Employee_Type, Contant_Info , salary):

    if is_id_exists(emp_list ,Employee_ID ):
        print("Error: Employee ID already exists")
        return emp_list
    
    employee_info = {
        "id":Employee_ID,"name":Name,
        "age":Age,"department":Department,
        "employee_type":Employee_Type , 
        "contact_info":Contant_Info
    }

    employee_info["bonus"] = 0
    employee_info["deduction"] = 0

    if Employee_Type == "Full_Time":
        employee_info["basic_salary"] = salary
        employee_info["absent_days"] = 0
        employee_info["late_days"] = 0
    elif Employee_Type == "Part_Time":
        employee_info["hourly_rate"] = salary
        employee_info["working_hours"] = 0
    elif Employee_Type == "Freelancer":
        employee_info["project_rate"] = salary
        employee_info["completed_projects"] = 0

    emp_list.append(employee_info)
    return emp_list

def display_all_employees(emp_list):
    if len(emp_list) == 0:
        print("No employees to display.")
        return

    print("========================================\n"
          "ALL EMPLOYEES\n"
          "========================================\n"
          "ID    Name         Type         Department    \n"
          "-------------------------------------------")

    for emp in emp_list:
        print(f"{emp['id']}     {emp['name']}     {emp['employee_type']}     {emp['department']}")

    print("--------------------------------------------")
    print(f"Total Employees: {len(emp_list)}")
    
def search_by_id(emp_list):
    while True:
        ID = int(input("Enter the ID: "))
        found = False
        for emp_id in emp_list:
            if emp_id['id'] == ID:
                print(f"Name: {emp_id['name']} | ID: {emp_id['id']} | Age: {emp_id['age']}")
                found = True
        if not found:
            print('not found')
            again = input("Search again? (y/n)")
            if again.lower() == 'n':
                break
        else:
            break
    
def search_by_name(emp_list):
    while True:
        name = input("Enter the Name: ")
        found = False
        for emp_name in emp_list:
            if emp_name['name'] == name:
                print(f"Name: {emp_name['name']} | ID: {emp_name['id']} | Age: {emp_name['age']}")
                found = True

        if not found:
            print("not found")
            again = input("Search again? (y/n): ")
            if again.lower() == 'n':
                break
        else:
            break

def search_by_department(emp_list):
    while True:
        department = input("Enter department: ")
        found = False
        for index , emp_department in enumerate(emp_list,start=1):
            if emp_department['department'].strip().lower() == department.strip().lower():
                print(f"{index}.Name: {emp_department['name']} | ID: {emp_department['id']} | Age: {emp_department['age']} | Department: {emp_department['department']}")
                found = True
        if not found:
            print(f"not found this Department: {department}")
            again = input("Search again? (y/n): ")
            if again.lower() == 'n':
                break
        else:
            break

def search_by_type(emp_list):
    while True:
        type_e = input("Enter the employee type: ").strip().lower()
        found = False
        for emp_type in emp_list:
            if emp_type['employee_type'].strip().lower() == type_e:
                print(f"Name: {emp_type['name']} | ID: {emp_type['id']} | Age: {emp_type['age']} | Department: {emp_type['department']} | Employee type: {emp_type['employee_type']}")
                found = True
        if not found:
            print(f"Not found this employee type: {type_e}")
            again = input("Search again? (y/n): ")
            if again.lower() == 'n':
                break
        else:
            break

def update_employee(emp_list):
    while True:
        ID = int(input("enter the id for search to update: ").strip())
        found = False
        for update in emp_list:
            if update['id'] == ID:
                found = True

                while True:
                    print("what you need update: \n"
                    "1.Name\n"
                    "2.ID\n"
                    "3.Age\n"
                    "4.Department\n"
                    "5.Employee type\n"
                    "6.contact\n"
                    "or done to exit")
                    choise = input("choise number: ").strip()

                    if choise.lower() == "done":
                        print("Done editing this employee.")
                        break   

                    elif int(choise) == 1:
                        update['name'] = input("enter the new Name: ").strip().capitalize()
                    elif int(choise) == 2:
                        update['id'] = int(input("enter the new ID: ").strip())
                    elif int(choise) == 3:
                        update['age'] = int(input("enter the new Age: ").strip())
                    elif int(choise) == 4:
                        update['department'] = input("enter the new Department: ").strip().capitalize()
                    elif int(choise) == 5:
                        update['employee_type'] = input("enter the new Employee type: ").strip().capitalize()
                    elif int(choise) == 6:
                        update['contact_info'] = input("enter the new contact for employee: ").strip().capitalize()
                    else:
                        print("Invalid choice, try again.")
                        continue   

                    
                    print("Employee updated successfully.")
                    print(f"Name: {update['name']} | ID: {update['id']} | Age: {update['age']} | "
                          f"Department: {update['department']} | Type: {update['employee_type']} | Contact: {update['contact_info']}")

                    again = input("Update another field for this employee? (y/n): ").strip().lower()
                    if again == 'n':
                        break   

                break   
        if not found:
            print("Not found this employee")
            again = input("Search again? (y/n): ")
            if again.lower() == 'n':
                break
        else:
            another = input("Update another employee? (y/n): ").strip().lower()
            if another == 'n':
                break
    save_data(emp_list)

def delete_employee(emp_list):
    while True:
        ID = int(input("Enter the ID for deleting: "))
        found = False
        for delete_emp in emp_list:
            if delete_emp['id'] == ID:
                found = True 
                print(delete_emp)
                choice = input("To delete the employee enter (y) to exit enter (n)").strip().lower()
                if choice == 'y':
                    emp_list.remove(delete_emp)
                    print("Employee deleted successfully.")   
                else:
                    print("Cancelled, employee not deleted.")
                break   
        if not found:
            print(f"Not found this employee")
            again = input("Search again? (y/n): ")
            if again.lower() == 'n':
                break
        else:
            another = input("You need Delete another employee? (y/n): ").strip().lower()
            if another == 'n':
                break
    save_data(emp_list)

def save_data(emp_list):
    with open("employee_data.json","w") as file:
        json.dump(emp_list,file,indent=4)

def load_data():
    try:
        with open("employee_data.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Employee file not found. A new employee database will be created.")
        return []
    except json.decoder.JSONDecodeError:
        print("Error while loading employee data.")
        print("Please check the employee file.")
        return []

def add_employee_flow(emp_list):
    while True:
        while True:
            try:
                id = int(input("Enter Employee ID: ").strip())
            except:
                print("Please enter a valid number")
                continue

            if is_id_exists(emp_list, id):
                print("Error: Employee ID already exists")
                continue

            break
        name = input("Enter Employee Name: ").strip().capitalize()

        while True:
            try:
                age = int(input("Enter Employee Age: ").strip())
                break
            except:
                print("Please enter a valid number")

        department = input("Enter Employee Department: ").strip().capitalize()
        contact = input("Enter Contact Info: ").strip()

        while True:
            print("Select Employee Type (1,2,3) : \n"
            "1.Full_Time\n"
            "2.Part_time\n"
            "3.Freelancer")
            emp_type_choice = input("--> ").strip()

            if emp_type_choice == '1':
                emp_type = 'Full_Time'
                while True:
                    try:
                        salary = float(input("Enter the Basic_Salary: "))
                        break
                    except:
                        print("Please enter a valid number.")
                break

            elif emp_type_choice == '2':
                emp_type = 'Part_Time'
                while True:
                    try:
                        salary = float(input("Enter the Hourly_Salary: "))
                        break
                    except:
                        print("Please enter a valid number.")
                break

            elif emp_type_choice == '3':
                emp_type = 'Freelancer'
                while True:
                    try:
                        salary = float(input("Enter the Project_rate: "))
                        break
                    except:
                        print("Please enter a valid number.")
                break

            else:
                print("Invalid employee type.")
                again = input("Do you want to try again? (y,n): ").strip().lower()
                if again == 'n':
                    return emp_list

        emp_list = Add_Eployee(emp_list , id , name , age , department , emp_type , contact , salary)
        save_data(emp_list)

        again = input("Do you need add anther Employee....?  (y,n): ").strip().lower()
        if again != 'y':
            return emp_list
            
def bonus_employee(emp_list):
    while True:
        while True:
            try:
                id = int(input("Enter id For Employee to ADD Bonus: ").strip())
                break
            except:
                print("Please enter a valid number.")
        found = False
        for bonus_emp in emp_list:
            if bonus_emp['id'] == id:
                found = True
                bonus = float(input("Enter the bonus: "))
                temp_bonus = bonus_emp["bonus"]
                bonus_emp["bonus"] += bonus
                print(f"Current bonus = {temp_bonus}\n"
                     f"new bonus entered = {bonus}\n"
                     f"total bonus = {bonus_emp['bonus']}\n")
        if not found:
            print("Employee not found")
            again = input("Search again? (y/n): ")
            if again.lower() == 'n':
                break
            else:
                continue

        again_2 = input("Do you want add Bonus for other employee (y/n) ? ").strip().lower()
        if again_2 == 'n':
            break
                    
    save_data(emp_list)

def deduction_employee(emp_list):
    while True:
        while True:
            try:
                id = int(input("Enter the id For Employee to ADD deduction: "))
                break
            except:
                print("Please enter a valid number.")
        found = False
        for deduction_emp in emp_list:
            if deduction_emp['id'] == id:
                found = True
                deduction = float(input("Enter the amount of deduction: "))
                temp_deduction = deduction_emp['deduction']
                deduction_emp['deduction'] += deduction
                print(f"Current deduction = {temp_deduction}\n"
                      f"New deduction entered = {deduction}\n"
                      f"thr total deduction = {deduction_emp['deduction']}")

        if not found:
            again = input("Not found you need try again (y | n) ? ").strip().lower()
            if again == 'n':
                break
            else:
                continue
        again_2 = input("Do you need add the new deduction for new employee (y | n) ? ").strip().lower()
        if again_2 == 'n':
            break
    save_data(emp_list)

def recored_attendance(emp_list):
    while True:
        while True:
            try:
                id = int(input("Enter the id For Employee to ADD Atendence: "))
                break
            except:
                print("Please enter a valid number.")
        found = False
        for attend in emp_list:
            if attend['id'] == id:
                found = True
                if attend['employee_type'] == 'Full_Time':
                    choice = input("Select from (1 | 2):\n"
                    "1.Absent Day\n"
                    "2.Late Day\n"
                    "-->")
                    if choice == '1':
                        attend["absent_days"] += 1
                        print(f"Attendance recorded successfully! \nTotal Absences Day: {attend['absent_days']}")
                    elif choice == '2':
                        attend["late_days"] += 1
                        print(f"Attendance recorded successfully! \nTotal Late Days: {attend['late_days']}")
                    else:
                        print("your choose incorrect")
                        break

                elif attend["employee_type"] == "Part_Time":
                    while True:
                        try:
                            houer_number = int(input("Enter the number of houre: "))
                            break
                        except:
                            print("Please enter a valid number")
                    attend["working_hours"] += houer_number
                    print(f"Attendance recorded successfully! \nTotal Working Houre: {attend['working_hours']}")

                elif attend["employee_type"] == "Freelancer":
                    attend["completed_projects"] += 1
                    print(f"Attendance recorded successfully! \nTotal Working Houre: {attend['completed_projects']}")
        if not found:
            again = input("Not found you need try again (y | n) ? ").strip().lower()
            if again == 'n':
                break
            else:
                continue

        again_2 = input("Do you need add a new Attendence for new employee (y | n) ? ").strip().lower()
        if again_2 == 'n':
            break

    save_data(emp_list)

def calculate_full_time_salary(emp_full_time):
    absence_deduction = emp_full_time["absent_days"] * 200
    late_deduction = emp_full_time["late_days"] * 50
    final_salary = emp_full_time["basic_salary"] + emp_full_time["bonus"] - emp_full_time["deduction"] - absence_deduction - late_deduction  
    return final_salary          

def calculate_part_time_salary(emp_part_time):
    salary = emp_part_time["hourly_rate"] * emp_part_time["working_hours"]
    final_salary = salary + emp_part_time["bonus"] - emp_part_time["deduction"]
    return final_salary

def calculate_freelancer_salary(freelancer_salary):
    salary = freelancer_salary["project_rate"] * freelancer_salary["completed_projects"]
    final_salary = salary + freelancer_salary["bonus"] - freelancer_salary["deduction"]
    return final_salary

def calculate_employee_salary(emp):
    if emp["employee_type"] == "Full_Time":
        return calculate_full_time_salary(emp)
    elif emp["employee_type"] == "Part_Time":
        return calculate_part_time_salary(emp)
    elif emp["employee_type"] == "Freelancer":
        return calculate_freelancer_salary(emp)

def display_salary_details(emp_list):
    while True:
        while True:
            try:
                id = int(input("Enter id For Employee to display salary details: ").strip())
                break 
            except:
                print("Please enter a valid number.")
        found = False
        for salary_details in emp_list:
            if salary_details['id'] == id:
                found = True
                final_salary = calculate_employee_salary(salary_details)
                print(f"========================================\n"
                       "SALARY DETAILS\n"
                       "========================================\n"
                       "\n"
                       f"Employee: {salary_details['name']}\n"
                       f"Employee Type: {salary_details['employee_type']}\n"
                       "\n")
                if  salary_details['employee_type'] == 'Full_Time':
                    print(f"Basic salary:{salary_details['basic_salary']}\n"
                          f"Bonus: {salary_details['bonus']}\n"
                          f"Deduction: {salary_details['deduction']}\n"
                          f"Absent day: {salary_details['absent_days']}\n"
                          f"Absence Deduction: {salary_details['absent_days'] * 200}\n"
                          f"Late day: {salary_details['late_days']}\n"
                          f"Late Deduction: {salary_details['late_days'] * 50}")
                elif salary_details['employee_type'] == 'Part_Time':
                    print(f"Hourly Rate: {salary_details['hourly_rate']}\n"
                          f"Working Hours: {salary_details['working_hours']}")
                elif salary_details['employee_type'] == 'Freelancer':
                    print(f"Project Rate: {salary_details['project_rate']}\n"
                          f"Completed Projects: {salary_details['completed_projects']}")

                print("----------------------------------------\n"
                      f"Final Salary: {final_salary}\n"
                      "========================================")

        if not found:
            again = input("Not found you need try again (y | n)? ").strip().lower()
            if again == 'n':
                break
            else:
                continue
        again_2 = input("To Desplay another salary (y | n)")
        if again_2 == 'n':
            break

def calculate_total_payroll(emp_list):
    total = 0
    for total_salary in emp_list:
        total += calculate_employee_salary(total_salary)
    return total

def calculate_average_salary(emp_list):
    if len(emp_list) == 0:
        return 0
    total = calculate_total_payroll(emp_list)
    return total / len(emp_list)

def find_highest_paid_employee(emp_list):
    if len(emp_list) == 0:
        return None

    highest_emp = emp_list[0]
    highest_salary = calculate_employee_salary(highest_emp)

    for emp in emp_list:
        current_salary = calculate_employee_salary(emp)
        if current_salary > highest_salary:
            highest_salary = current_salary
            highest_emp = emp

    return highest_emp

def find_lowest_paid_employee(emp_list):
    if len(emp_list) == 0:
        return None

    lowest_emp = emp_list[0]
    lowest_salary = calculate_employee_salary(lowest_emp)

    for emp in emp_list:
        current_salary = calculate_employee_salary(emp)
        if current_salary < lowest_salary:
            lowest_salary = current_salary
            lowest_emp = emp

    return lowest_emp

def payroll_report(emp_list):
    if len(emp_list) == 0:
        print("No employees to display.")
        return

    print("========================================\n"
          "MONTHLY PAYROLL REPORT\n"
          "========================================\n"
          "\nID     Name    Type           Final Salary\n"
          "--------------------------------------------------")

    for all_emp in emp_list:
        final_salary = calculate_employee_salary(all_emp)
        print(f"{all_emp['id']}      {all_emp['name']}     {all_emp['employee_type']}      {final_salary}")

    print("--------------------------------------------------")

    total_payroll = calculate_total_payroll(emp_list)
    average_salary = calculate_average_salary(emp_list)
    print(f"Total Payroll: {total_payroll} EGP")
    print(f"Average Salary: {average_salary} EGP")

    highest_paid = find_highest_paid_employee(emp_list)
    lowest_paid = find_lowest_paid_employee(emp_list)

    print(f"\nHighest Paid Employee:")
    print(f"{highest_paid['name']} - {calculate_employee_salary(highest_paid)} EGP")

    print(f"\nLowest Paid Employee:")
    print(f"{lowest_paid['name']} - {calculate_employee_salary(lowest_paid)} EGP")

def display_statistics(emp_list):
    if len(emp_list) == 0:
        print("No employees to display.")
        return

    total_employees = len(emp_list)

    full_time_count = 0
    part_time_count = 0
    freelancer_count = 0
    departments = {}

    for emp in emp_list:
        if emp['employee_type'] == 'Full_Time':
            full_time_count += 1
        elif emp['employee_type'] == 'Part_Time':
            part_time_count += 1
        elif emp['employee_type'] == 'Freelancer':
            freelancer_count += 1

        dept = emp['department']
        if dept in departments:
            departments[dept] += 1
        else:
            departments[dept] = 1

    total_payroll = calculate_total_payroll(emp_list)
    average_salary = calculate_average_salary(emp_list)

    print("========================================\n"
          "EMPLOYEE STATISTICS\n"
          "========================================\n")

    print(f"Total Employees: {total_employees}\n")

    print(f"Full-Time Employees: {full_time_count}")
    print(f"Part-Time Employees: {part_time_count}")
    print(f"Freelancers: {freelancer_count}\n")

    for dept, count in departments.items():
        print(f"{dept} Department: {count}")

    print(f"\nTotal Payroll: {total_payroll} EGP")
    print(f"Average Salary: {average_salary} EGP")
