import csv

import mysql.connector
from Tools.scripts.make_ctype import values


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="KiR@nC76@29_12",
        database="employee_db"
    )
class Employee:

    def __init__(self, emp_id, emp_name, designation, basic, hra, da, deduction):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.designation = designation
        self.basic =basic
        self.hra = hra
        self.da = da
        self.deduction = deduction
        self.net_salary = self.calculate_net_salary()

    def calculate_net_salary(self):
        return self.basic + self.hra + self.da - self.deduction

    def display_payslip(self):
        print(f"--- Payslip for {self.emp_name} ({self.emp_id}) ---")
        print(f" Designation : {self.designation}")
        print(f" Basic pay : ₹{self.basic}")
        print(f" HRA : ₹{self.hra}")
        print(f" DA : ₹{self.da}")
        print(f" Deduction : ₹{self.deduction}")
        print(f" Net salary : ₹{self.net_salary}")

    def to_dict(self):
        return {
            "emp_id" : self.emp_id,
            "emp_name" : self.emp_name,
            "designation": self.designation,
            "basic" : self.basic,
            "hra" : self.hra,
            "da" : self.da,
            "deduction" : self.deduction,
            "net_salary" : self.net_salary
        }
employee_list = []

def add_employee():

    print("\nEnter Employee Details: ")
    emp_id = input("Employee ID: ")
    emp_name = input("Employee Name: ")
    designation = input("Designation: ")
    basic = float(input("Basic Pay: "))
    hra = float(input("HRA: "))
    da = float(input("DA: "))
    deduction = float(input("Deduction: "))

    employee = Employee(emp_id, emp_name, basic, designation, hra, da, deduction)
    employee_list.append(employee)
    save_employee_to_mysql(employee)
    print("\n✅ Employee added successfully!\n")

def view_all_payslips():
    if not employee_list:
        print("\n⚠️ No employees found.\n")
        return

    for employee in employee_list:
        employee.display_payslip()
        print("-" * 30)

def save_employee_to_mysql(employee):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO employees (emp_id, emp_name, designation, basic, hra, da, deduction, net_salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        emp_name = VALUES(emp_name),
        designation = VALUES(designation),
        basic = VALUES(basic),
        hra = VALUES(hra),
        da = VALUES(da),
        deduction = VALUES(deduction),
        net_salary = VALUES(net_salary)
    """
    values = (
        employee.emp_id, employee.emp_name,
        employee.designation, employee.basic,
        employee.hra, employee.da, employee.deduction, employee.net_salary
    )
    cur.execute(query, values)
    conn.commit()
    conn.close()

def save_all_employees_to_mysql(emp_list):
    for emp in emp_list:
        save_employee_to_mysql(emp)
    print("✅ All employees saved to MySQL.")


def export_employees_to_csv(filename="employees_data.csv"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT emp_id, emp_name, designation, basic, hra, da, deduction, net_salary FROM employees")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("⚠️ No employee records to export.")
        return

    # Define headers
    headers = ["Employee ID", "Name", "Designation", "Basic Pay", "HRA", "DA", "Deduction", "Net Salary"]

    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"✅ Employee data exported to '{filename}' successfully.")


def load_employees_from_mysql():
    employee_list.clear()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()

    for row in rows:
        try:
            emp = Employee(
                row[0],                     # emp_id (string)
                row[1],                     # name
                row[2],                     # designation
                float(row[3]),              # basic
                float(row[4]),              # hra
                float(row[5]),              # da
                float(row[6])               # deduction
            )
            employee_list.append(emp)
        except Exception as e:
            print(f"⚠️ Failed to load record: {row} → Error: {e}")

    conn.close()

def search_employee():
    if not employee_list:
        print("\n⚠️ No employee records to search.\n")
        return

    search_by = input("Search by (1: ID, 2: Name): ")

    if search_by == '1':
        emp_id = input("Enter Employee ID to Search: ")
        found = False

        for employee in employee_list:
            if employee.emp_id.lower() == emp_id.lower():
                employee.display_payslip()
                found = True
                break

        if not found:
            print("❌ Employee ID not found.")

    elif search_by == '2':
        emp_name = input("Enter Employee Name to Search: ")
        found = False

        for employee in employee_list:
            if employee.emp_name.lower() == emp_name.lower():
                employee.display_payslip()
                found = True
                break
        if not found:
            print("❌ Employee Name not found.")

    else:
        print("❌ Invalid option. Please choose 1 or 2.")
search_employee()

def update_employee_in_mysql(emp_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
    result = cur.fetchone()
    if not result:
        print("❌ Employee ID not found.")
        conn.close()
        return

    print("Enter new values (Leave blank to keep existing): ")
    emp_name = input(f"Name [{result[1]}]: ") or result[1]
    designation = input(f"Designation [{result[2]}]: ") or result[2]

    try:
        basic = input(f"Basic Pay [{result[3]}]: ")
        hra = input(f"HRA [{result[4]}]: ")
        da = input(f"DA [{result[5]}]: ")
        deduction = input(f"Deductions [{result[6]}]: ")

        basic = float(basic) if basic else result[3]
        hra = float(hra) if hra else result[4]
        da = float(da) if da else result[5]
        deduction = float(deduction) if deduction else result[6]

        net_salary = basic + hra + da - deduction

        cur.execute("""
            UPDATE employees
            SET emp_name=%s, designation=%s, basic=%s, hra=%s, da=%s, deduction=%s, net_salary=%s
            WHERE emp_id=%s
        """, (emp_name, designation, basic, hra, da, deduction, net_salary, emp_id))

        conn.commit()
        print("✅ Employee updated successfully.\n")
    except ValueError:
        print("❌ Invalid input. Update cancelled.")
    conn.close()


def delete_employee_from_mysql(emp_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
    result = cur.fetchone()

    if not result:
        print("❌ Employee ID not found.")
    else:
        confirm = input("Are you sure you want to delete this employee? (y/n): ")
        if confirm.lower() == 'y':
            cur.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
            conn.commit()
            print("🗑️ Employee deleted successfully.\n")
        else:
            print("❎ Deletion cancelled.")

    conn.close()

def main_menu():
    global employee_list
    load_employees_from_mysql()

    print("=========================================")
    print("📂 EMPLOYEES LOADED FROM DATABASE")
    print("=========================================")
    view_all_payslips()
    print("=========================================")

    while True:
        print("\n === Employee Salary Management System ===")
        print("1. Add New Employee")
        print("2. View All Payslips")
        print("3. Search Employee")
        print("4. Update/Delete Employee")
        print("5. Save")
        print("6. Exit")
        print("7. Export Employees to CSV")
        print("8. Reload Data from Database")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_employee()
        elif choice == '2':
            view_all_payslips()
        elif choice == '3':
            search_employee()
        elif choice == '4':
            emp_id = input("Enter Employee ID to update or delete: ")
            print("1. Update\n2. Delete")
            sub_choice = input("Choose an action: ")

            if sub_choice == '1':
                update_employee_in_mysql(emp_id)
            elif sub_choice == '2':
                delete_employee_from_mysql(emp_id)
            else:
                print("❌ Invalid option.")

        elif choice == '5':
            save_all_employees_to_mysql(employee_list)
        elif choice == '6':
            save_all_employees_to_mysql(employee_list)
            print("Exiting the Program. Bye!")
        elif choice == '7':
            export_employees_to_csv()
        elif choice == '8':
            load_employees_from_mysql()
        else:
            print("Invalid choice. Try again")
main_menu()