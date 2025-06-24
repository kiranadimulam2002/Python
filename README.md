🧾 Employee Salary Management System (Console-Based)

This is a **Python-based console application** for managing employee salary records. It allows users to add, view, search, update, delete, and export employee salary data. The application uses **MySQL** for persistent storage and also provides options to export data to CSV.

---

## 🚀 Features

- ➕ Add new employee records
- 🧾 View individual payslips and all employees
- 🔍 Search employee by ID or name
- 🔄 Update or delete employee records
- 💾 Save and load data to/from MySQL database
- 📤 Export all employee records to `.csv` file
- 🖥️ View data on console every time program starts
- 🔁 Manual reload from database


🛠️ Tech Stack

- **Language**: Python 3
- **Database**: MySQL
- **File Export**: CSV using Python's built-in `csv` module

📁 Folder Structure

Employee-Salary-Management-System/
├── Employee.py              # Main Python application
├── README.md                # Project documentation
└── employees\_data.csv       # (Optional) Exported CSV file

🔧 Prerequisites

- Python 3.x
- MySQL Server running and accessible
- Python packages:
  - `mysql-connector-python`

Install using:

```bash
pip install mysql-connector-python
````

---

🧮 MySQL Setup

Run the following SQL to set up the database and table:

```sql
CREATE DATABASE employee_db;

USE employee_db;

CREATE TABLE employees (
    emp_id VARCHAR(10) PRIMARY KEY,
    emp_name VARCHAR(100),
    designation VARCHAR(100),
    basic FLOAT,
    hra FLOAT,
    da FLOAT,
    deduction FLOAT,
    net_salary FLOAT
);
```

---
▶️ How to Run

1. Clone this repository:

```bash
git clone https://github.com/yourusername/employee-salary-management.git
cd employee-salary-management
```

2. Open `Employee.py` and **configure your MySQL credentials** inside `get_db_connection()`:

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password",
        database="employee_db"
    )
```

3. Run the program:

```bash
python Employee.py
```

📤 Exported Data

When exporting, the employee records are saved in `employees_data.csv`. Ensure no other program (like Excel) is keeping the file open while exporting.

✅ TODO / Future Enhancements

[ ] Add support for Excel (`.xlsx`) export using `openpyxl`
[ ] Add login system (Admin/User)
[ ] GUI version using Tkinter or PyQt
[ ] Sort/filter employees by role or salary
[ ] Integrate with cloud DB (e.g., Firebase, MongoDB Atlas)

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📄 License

This project is licensed under the [MIT License](LICENSE).

✨ Acknowledgements

Developed by Satya Sai Kiran Adimulam
