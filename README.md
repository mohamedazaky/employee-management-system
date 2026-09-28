# Employee Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.60%2B-FF4B4B?logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.0%2B-150458?logo=pandas&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A payroll and HR records system for a small company with three kinds of staff: **full-time**, **part-time** and **freelancers**. It ships with two interfaces built on the same business logic:

- **Web dashboard** (Streamlit): company overview, searchable employee table, add/edit forms and a payroll report with CSV export.
- **Console app**: a menu-driven terminal program covering every operation.

![Overview](screenshots/overview.png)

## Features

- **Employee records**: add, edit and delete employees, with validation (unique IDs, valid ages, positive pay rates)
- **Search and filter** by ID, name, department or employee type
- **Three pay models**, each with its own salary rules (see [How salaries are calculated](#how-salaries-are-calculated))
- **Bonuses and deductions** for any employee
- **Attendance tracking**: absences, late days, hours worked and completed projects
- **Payroll**: a salary slip for each employee and a monthly payroll report you can export to CSV
- **Statistics**: headcount by type and department, total and average payroll
- **Saves automatically** to a local JSON file, so there's no database to set up

| Employees | Payroll |
|---|---|
| ![Employees](screenshots/employees.png) | ![Payroll](screenshots/payroll.png) |

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web UI | [Streamlit](https://streamlit.io/) |
| Data handling | [pandas](https://pandas.pydata.org/) |
| Storage | JSON file (`employee_data.json`) |
| Console UI | Python standard library |

## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip

### Installation

```bash
git clone https://github.com/mohamedazaky/employee-management-system.git
cd employee-management-system
pip install -r requirements.txt
```

Using a virtual environment is recommended:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the web dashboard

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`. On Windows you can also double-click `run_app.bat`. It installs the requirements and launches the dashboard.

### Run the console app

```bash
python main.py
```

## How salaries are calculated

| Type | Formula |
|---|---|
| Full-time | `basic salary + bonus − deduction − (200 EGP × absent days) − (50 EGP × late days)` |
| Part-time | `hourly rate × hours worked + bonus − deduction` |
| Freelancer | `project rate × completed projects + bonus − deduction` |

## Project Structure

```
employee-management-system/
├── app.py                  # Streamlit web dashboard
├── main.py                 # Console menu entry point
├── employee_functions.py   # Business logic: CRUD, salary rules, search, storage
├── employee_data.json      # Sample data
├── run_app.bat             # Windows one-click launcher for the dashboard
├── .streamlit/config.toml  # Dashboard theme
├── screenshots/            # Images used in this README
└── requirements.txt
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Author

**Mohamed Zaky**, [@mohamedazaky](https://github.com/mohamedazaky)
