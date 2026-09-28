"""Web interface for the Employee Management System.

Run with:  streamlit run app.py
All business logic lives in employee_functions.py (shared with the console app in main.py).
"""
import pandas as pd
import streamlit as st

from employee_functions import (
    ABSENCE_DEDUCTION,
    EMPLOYEE_TYPES,
    LATE_DEDUCTION,
    RATE_FIELD,
    add_bonus,
    add_deduction,
    add_employee,
    format_department,
    calculate_employee_salary,
    delete_employee_by_id,
    filter_employees,
    find_employee,
    find_highest_paid_employee,
    get_rate,
    get_statistics,
    is_id_exists,
    load_data,
    next_employee_id,
    reset_type_fields,
    save_data,
)

st.set_page_config(page_title="Employee Management System", page_icon="🗂️", layout="wide")

TYPE_LABELS = {"Full_Time": "Full-time", "Part_Time": "Part-time", "Freelancer": "Freelancer"}
RATE_LABELS = {
    "Full_Time": "Monthly salary (EGP)",
    "Part_Time": "Hourly rate (EGP)",
    "Freelancer": "Rate per project (EGP)",
}

st.markdown(
    """
    <style>
    .block-container {padding-top: 2.2rem; max-width: 1200px;}
    [data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #D5DED9; border-radius: 10px; padding: 14px 18px;
    }
    [data-testid="stMetricValue"] {font-variant-numeric: tabular-nums; font-size: 1.55rem;}
    .slip {background:#FFFFFF; border:1px solid #D5DED9; border-radius:10px; padding:18px 22px;}
    .slip table {width:100%; border-collapse:collapse; border:none !important; font-variant-numeric: tabular-nums;}
    .slip td {padding:6px 0 !important; border:none !important; border-bottom:1px dashed #D5DED9 !important; background:transparent !important;}
    .slip td:last-child {text-align:right;}
    .slip tr.minus td:last-child {color:#A23B2A;}
    .slip tr.total td {border-bottom:none !important; border-top:2px solid #1C2321 !important; font-weight:700; font-size:1.1rem; padding-top:10px;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------
# State helpers
# ----------------------------------------

if "emp_list" not in st.session_state:
    st.session_state.emp_list = load_data()

emp_list = st.session_state.emp_list


def commit(message):
    """Save to disk and show a confirmation after the page reloads."""
    save_data(emp_list)
    st.session_state.flash = message
    st.rerun()


if "flash" in st.session_state:
    st.toast(st.session_state.pop("flash"), icon="✅")


def money(value):
    return f"{value:,.2f} EGP"


def employees_frame(employees):
    rows = []
    for emp in employees:
        rows.append({
            "ID": emp["id"],
            "Name": emp["name"],
            "Department": emp["department"],
            "Type": TYPE_LABELS.get(emp["employee_type"], emp["employee_type"]),
            "Age": emp["age"],
            "Contact": emp["contact_info"],
            "Final salary (EGP)": calculate_employee_salary(emp),
        })
    return pd.DataFrame(rows)


def salary_lines(emp):
    """(label, amount) pairs that make up the final salary."""
    t = emp["employee_type"]
    if t == "Full_Time":
        lines = [
            ("Basic salary", emp["basic_salary"]),
            ("Bonus", emp["bonus"]),
            ("Deductions", -emp["deduction"]),
            (f"Absence ({emp['absent_days']} × {ABSENCE_DEDUCTION})", -emp["absent_days"] * ABSENCE_DEDUCTION),
            (f"Late days ({emp['late_days']} × {LATE_DEDUCTION})", -emp["late_days"] * LATE_DEDUCTION),
        ]
    elif t == "Part_Time":
        lines = [
            (f"Hours ({emp['working_hours']} × {emp['hourly_rate']:,.2f})", emp["working_hours"] * emp["hourly_rate"]),
            ("Bonus", emp["bonus"]),
            ("Deductions", -emp["deduction"]),
        ]
    else:
        lines = [
            (f"Projects ({emp['completed_projects']} × {emp['project_rate']:,.2f})",
             emp["completed_projects"] * emp["project_rate"]),
            ("Bonus", emp["bonus"]),
            ("Deductions", -emp["deduction"]),
        ]
    return lines


def render_slip(emp):
    rows = ""
    for label, amount in salary_lines(emp):
        css = "minus" if amount < 0 else ""
        rows += f"<tr class='{css}'><td>{label}</td><td>{amount:,.2f}</td></tr>"
    rows += f"<tr class='total'><td>Final salary</td><td>{money(calculate_employee_salary(emp))}</td></tr>"
    st.markdown(
        f"<div class='slip'><b>{emp['name']}</b> · {TYPE_LABELS[emp['employee_type']]} · {emp['department']}"
        f"<table style='margin-top:10px'>{rows}</table></div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------
# Pages
# ----------------------------------------

def overview_page():
    st.title("Overview")
    if not emp_list:
        st.info("No employees yet. Add your first employee from the **Add employee** page.")
        return

    stats = get_statistics(emp_list)
    top = find_highest_paid_employee(emp_list)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees", stats["total_employees"])
    c2.metric("Monthly payroll", money(stats["total_payroll"]))
    c3.metric("Average salary", money(stats["average_salary"]))
    c4.metric("Highest paid", top["name"].split()[0], money(calculate_employee_salary(top)), delta_color="off", delta_arrow="off")

    st.write("")
    left, right = st.columns([3, 2])
    df = employees_frame(emp_list)

    with left:
        st.subheader("Payroll by department")
        by_dept = df.groupby("Department")["Final salary (EGP)"].sum().sort_values(ascending=False)
        st.bar_chart(by_dept, horizontal=True, color="#2F6B4F", height=300)

    with right:
        st.subheader("Headcount by type")
        counts = pd.Series(
            {TYPE_LABELS[t]: n for t, n in stats["type_counts"].items()}, name="Employees"
        )
        st.bar_chart(counts, horizontal=True, color="#8FB8A2", height=300)


def employees_page():
    st.title("Employees")
    if not emp_list:
        st.info("No employees yet. Add your first employee from the **Add employee** page.")
        return

    departments = sorted({emp["department"] for emp in emp_list})
    f1, f2, f3 = st.columns([2, 1, 1])
    name = f1.text_input("Search by name", placeholder="Type part of a name")
    dept = f2.selectbox("Department", ["All"] + departments)
    etype = f3.selectbox("Type", ["All"] + EMPLOYEE_TYPES, format_func=lambda t: TYPE_LABELS.get(t, t))

    results = filter_employees(
        emp_list,
        name=name,
        department="" if dept == "All" else dept,
        employee_type="" if etype == "All" else etype,
    )

    if not results:
        st.warning("No employees match these filters.")
        return

    event = st.dataframe(
        employees_frame(results),
        hide_index=True,
        width="stretch",
        on_select="rerun",
        selection_mode="single-row",
        column_config={"Final salary (EGP)": st.column_config.NumberColumn(format="localized")},
        key="emp_table",
    )
    st.caption(f"{len(results)} of {len(emp_list)} employees · select a row to manage that employee")

    selected = event.selection.rows
    if not selected:
        return

    emp = find_employee(emp_list, results[selected[0]]["id"])
    st.divider()
    manage_employee(emp)


def manage_employee(emp):
    st.subheader(f"{emp['name']}  ·  ID {emp['id']}")
    tab_salary, tab_pay, tab_attend, tab_edit, tab_delete = st.tabs(
        ["Salary", "Bonus & deduction", "Attendance", "Edit details", "Delete"]
    )

    with tab_salary:
        render_slip(emp)

    with tab_pay:
        c1, c2 = st.columns(2)
        with c1.form(f"bonus_{emp['id']}", clear_on_submit=True):
            st.markdown(f"**Bonus** · current total {money(emp['bonus'])}")
            amount = st.number_input("Amount (EGP)", min_value=0.0, step=100.0, key=f"b_{emp['id']}")
            if st.form_submit_button("Add bonus", type="primary"):
                if amount <= 0:
                    st.error("Enter an amount greater than 0.")
                else:
                    add_bonus(emp, amount)
                    commit(f"Added {money(amount)} bonus to {emp['name']}")
        with c2.form(f"deduction_{emp['id']}", clear_on_submit=True):
            st.markdown(f"**Deduction** · current total {money(emp['deduction'])}")
            amount = st.number_input("Amount (EGP)", min_value=0.0, step=100.0, key=f"d_{emp['id']}")
            if st.form_submit_button("Add deduction"):
                if amount <= 0:
                    st.error("Enter an amount greater than 0.")
                else:
                    add_deduction(emp, amount)
                    commit(f"Added {money(amount)} deduction to {emp['name']}")

    with tab_attend:
        t = emp["employee_type"]
        if t == "Full_Time":
            st.write(f"Absent days: **{emp['absent_days']}** · Late days: **{emp['late_days']}**")
            st.caption(f"Each absent day deducts {ABSENCE_DEDUCTION} EGP, each late day {LATE_DEDUCTION} EGP.")
            a, b, _ = st.columns([1, 1, 3])
            if a.button("Record absent day", key=f"abs_{emp['id']}"):
                emp["absent_days"] += 1
                commit(f"Absent day recorded for {emp['name']}")
            if b.button("Record late day", key=f"late_{emp['id']}"):
                emp["late_days"] += 1
                commit(f"Late day recorded for {emp['name']}")
        elif t == "Part_Time":
            st.write(f"Working hours this month: **{emp['working_hours']}**")
            with st.form(f"hours_{emp['id']}", clear_on_submit=True):
                hours = st.number_input("Hours worked", min_value=1, max_value=300, step=1)
                if st.form_submit_button("Add hours", type="primary"):
                    emp["working_hours"] += int(hours)
                    commit(f"Added {int(hours)} hours for {emp['name']}")
        else:
            st.write(f"Completed projects: **{emp['completed_projects']}**")
            if st.button("Record completed project", key=f"proj_{emp['id']}", type="primary"):
                emp["completed_projects"] += 1
                commit(f"Project recorded for {emp['name']}")

    with tab_edit:
        with st.form(f"edit_{emp['id']}"):
            c1, c2 = st.columns(2)
            new_name = c1.text_input("Name", emp["name"])
            new_id = c2.number_input("Employee ID", min_value=1, value=int(emp["id"]), step=1)
            new_age = c1.number_input("Age", min_value=16, max_value=80, value=int(emp["age"]), step=1)
            new_dept = c2.text_input("Department", emp["department"])
            new_contact = c1.text_input("Contact info", emp["contact_info"])
            new_type = c2.selectbox(
                "Employee type", EMPLOYEE_TYPES,
                index=EMPLOYEE_TYPES.index(emp["employee_type"]),
                format_func=TYPE_LABELS.get,
            )
            new_rate = st.number_input(
                "Pay rate (EGP) — monthly salary, hourly rate or rate per project depending on type",
                min_value=0.0, value=float(get_rate(emp)), step=100.0,
            )
            if new_type != emp["employee_type"]:
                st.caption("Changing the type resets attendance, hours and projects for this employee.")

            if st.form_submit_button("Save changes", type="primary"):
                if not new_name.strip() or not new_dept.strip():
                    st.error("Name and department can't be empty.")
                elif new_id != emp["id"] and is_id_exists(emp_list, int(new_id)):
                    st.error(f"ID {int(new_id)} is already used by another employee.")
                else:
                    emp["name"] = new_name.strip().title()
                    emp["id"] = int(new_id)
                    emp["age"] = int(new_age)
                    emp["department"] = format_department(new_dept)
                    emp["contact_info"] = new_contact.strip()
                    if new_type != emp["employee_type"]:
                        reset_type_fields(emp, new_type, new_rate)
                    else:
                        emp[RATE_FIELD[new_type]] = new_rate
                    commit(f"Saved changes for {emp['name']}")

    with tab_delete:
        st.write(f"This permanently removes **{emp['name']}** and their payroll record.")
        confirm = st.checkbox("I understand this can't be undone", key=f"confirm_{emp['id']}")
        if st.button("Delete employee", disabled=not confirm, key=f"del_{emp['id']}"):
            name = emp["name"]
            delete_employee_by_id(emp_list, emp["id"])
            commit(f"Deleted {name}")


def add_page():
    st.title("Add employee")

    emp_type = st.segmented_control(
        "Employee type", EMPLOYEE_TYPES, default="Full_Time", format_func=TYPE_LABELS.get
    ) or "Full_Time"

    with st.form("add_employee", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full name")
        emp_id = c2.number_input("Employee ID", min_value=1, value=next_employee_id(emp_list), step=1)
        age = c1.number_input("Age", min_value=16, max_value=80, value=25, step=1)
        department = c2.text_input("Department", placeholder="e.g. Finance")
        contact = c1.text_input("Contact info", placeholder="Phone or email")
        rate = c2.number_input(RATE_LABELS[emp_type], min_value=0.0, step=100.0)

        if st.form_submit_button("Add employee", type="primary"):
            if not name.strip() or not department.strip():
                st.error("Name and department are required.")
            elif is_id_exists(emp_list, int(emp_id)):
                st.error(f"ID {int(emp_id)} is already used. Try {next_employee_id(emp_list)}.")
            elif rate <= 0:
                st.error(f"{RATE_LABELS[emp_type]} must be greater than 0.")
            else:
                add_employee(emp_list, int(emp_id), name.strip().title(), int(age),
                             format_department(department), emp_type, contact.strip(), rate)
                commit(f"Added {name.strip().title()}")


def payroll_page():
    st.title("Monthly payroll")
    if not emp_list:
        st.info("No employees yet. Add your first employee from the **Add employee** page.")
        return

    rows = []
    for emp in emp_list:
        t = emp["employee_type"]
        if t == "Full_Time":
            base = emp["basic_salary"]
            attendance = -(emp["absent_days"] * ABSENCE_DEDUCTION + emp["late_days"] * LATE_DEDUCTION)
        elif t == "Part_Time":
            base = emp["hourly_rate"] * emp["working_hours"]
            attendance = 0
        else:
            base = emp["project_rate"] * emp["completed_projects"]
            attendance = 0
        rows.append({
            "ID": emp["id"],
            "Name": emp["name"],
            "Type": TYPE_LABELS[t],
            "Department": emp["department"],
            "Base pay": base,
            "Bonus": emp["bonus"],
            "Deductions": -emp["deduction"],
            "Attendance": attendance,
            "Final salary": calculate_employee_salary(emp),
        })
    df = pd.DataFrame(rows)

    stats = get_statistics(emp_list)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total payroll", money(stats["total_payroll"]))
    c2.metric("Average salary", money(stats["average_salary"]))
    c3.metric("Total bonuses", money(df["Bonus"].sum()))

    money_col = st.column_config.NumberColumn(format="localized")
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={c: money_col for c in ["Base pay", "Bonus", "Deductions", "Attendance", "Final salary"]},
    )

    st.download_button(
        "Download payroll (CSV)",
        df.to_csv(index=False).encode("utf-8-sig"),
        file_name="payroll_report.csv",
        mime="text/csv",
    )


# ----------------------------------------
# Navigation
# ----------------------------------------

pages = [
    st.Page(overview_page, title="Overview", icon=":material/space_dashboard:", default=True),
    st.Page(employees_page, title="Employees", icon=":material/group:", url_path="employees"),
    st.Page(add_page, title="Add employee", icon=":material/person_add:", url_path="add"),
    st.Page(payroll_page, title="Payroll", icon=":material/payments:", url_path="payroll"),
]

with st.sidebar:
    st.markdown("### Employee Management")
    st.caption("Payroll, attendance and records for full-time, part-time and freelance staff.")

st.navigation(pages).run()
