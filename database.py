import sqlite3


DATABASE_NAME = "employees.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            department TEXT NOT NULL,

            salary REAL NOT NULL,

            city TEXT NOT NULL

        )
    """)

    connection.commit()

    connection.close()


def create_employee(
    name,
    email,
    department,
    salary,
    city
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO employees
            (name, email, department, salary, city)

            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            department,
            salary,
            city
        ))

        connection.commit()

        return {
            "success": True,
            "message": "Employee created successfully.",
            "id": cursor.lastrowid
        }

    except sqlite3.IntegrityError:

        return {
            "success": False,
            "message": "Email already exists."
        }

    finally:

        connection.close()


def get_employee(employee_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE id = ?
    """, (employee_id,))

    employee = cursor.fetchone()

    connection.close()

    if employee is None:
        return None

    return dict(employee)


def get_all_employees():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        ORDER BY id
    """)

    employees = cursor.fetchall()

    connection.close()

    return [
        dict(employee)
        for employee in employees
    ]


def update_employee(
    employee_id,
    name,
    email,
    department,
    salary,
    city
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE employees

            SET
                name = ?,
                email = ?,
                department = ?,
                salary = ?,
                city = ?

            WHERE id = ?
        """, (
            name,
            email,
            department,
            salary,
            city,
            employee_id
        ))

        connection.commit()

        if cursor.rowcount == 0:

            return {
                "success": False,
                "message": "Employee not found."
            }

        return {
            "success": True,
            "message": "Employee updated successfully."
        }

    except sqlite3.IntegrityError:

        return {
            "success": False,
            "message": "Email already exists."
        }

    finally:

        connection.close()


def delete_employee(employee_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (employee_id,))

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    if rows_deleted == 0:

        return {
            "success": False,
            "message": "Employee not found."
        }

    return {
        "success": True,
        "message": "Employee deleted successfully."
    }


def search_by_name(name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE name LIKE ?
        ORDER BY name
    """, (f"%{name}%",))

    employees = cursor.fetchall()

    connection.close()

    return [dict(employee) for employee in employees]


def search_by_department(department):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE department = ?
        ORDER BY name
    """, (department,))

    employees = cursor.fetchall()

    connection.close()

    return [dict(employee) for employee in employees]


def search_by_city(city):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE city = ?
        ORDER BY name
    """, (city,))

    employees = cursor.fetchall()

    connection.close()

    return [dict(employee) for employee in employees]


def search_by_salary(
    minimum_salary,
    maximum_salary
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees

        WHERE salary BETWEEN ? AND ?

        ORDER BY salary DESC
    """, (
        minimum_salary,
        maximum_salary
    ))

    employees = cursor.fetchall()

    connection.close()

    return [dict(employee) for employee in employees]


def count_employees():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
    """)

    result = cursor.fetchone()

    connection.close()

    return result["total"]


def highest_salary():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees

        ORDER BY salary DESC

        LIMIT 1
    """)

    employee = cursor.fetchone()

    connection.close()

    if employee is None:
        return None

    return dict(employee)


def search_department_salary(
    department,
    minimum_salary
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees

        WHERE department = ?
        AND salary >= ?

        ORDER BY salary DESC
    """, (
        department,
        minimum_salary
    ))

    employees = cursor.fetchall()

    connection.close()

    return [dict(employee) for employee in employees]
