import json
import os

from openai import OpenAI

from database import (
    count_employees,
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee,
    highest_salary,
    search_by_city,
    search_by_department,
    search_by_name,
    search_by_salary,
    search_department_salary,
    update_employee,
)


def _tool(name, description, properties=None, required=()):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties or {},
                "required": list(required),
                "additionalProperties": False,
            },
        },
    }


_TOOLS = [
    _tool("create_employee", "Create an employee. Ask for missing required details.", {
        "name": {"type": "string"}, "email": {"type": "string"},
        "department": {"type": "string"}, "salary": {"type": "number"},
        "city": {"type": "string"},
    }, ("name", "email", "department", "salary", "city")),
    _tool("get_employee", "Get one employee by ID.", {
        "employee_id": {"type": "integer"},
    }, ("employee_id",)),
    _tool("get_all_employees", "List all employees."),
    _tool("update_employee", "Replace an employee's details. Ask for missing required details.", {
        "employee_id": {"type": "integer"}, "name": {"type": "string"},
        "email": {"type": "string"}, "department": {"type": "string"},
        "salary": {"type": "number"}, "city": {"type": "string"},
    }, ("employee_id", "name", "email", "department", "salary", "city")),
    _tool("delete_employee", "Delete an employee by ID.", {
        "employee_id": {"type": "integer"},
    }, ("employee_id",)),
    _tool("search_by_name", "Find employees by a name fragment.", {
        "name": {"type": "string"},
    }, ("name",)),
    _tool("search_by_department", "Find employees in a department.", {
        "department": {"type": "string"},
    }, ("department",)),
    _tool("search_by_city", "Find employees in a city.", {
        "city": {"type": "string"},
    }, ("city",)),
    _tool("search_by_salary", "Find employees within a salary range.", {
        "minimum_salary": {"type": "number"},
        "maximum_salary": {"type": "number"},
    }, ("minimum_salary", "maximum_salary")),
    _tool("count_employees", "Count all employees."),
    _tool("highest_salary", "Find the employee with the highest salary."),
    _tool("search_department_salary", "Find department employees earning at least a salary.", {
        "department": {"type": "string"}, "minimum_salary": {"type": "number"},
    }, ("department", "minimum_salary")),
]

_FUNCTIONS = {
    "create_employee": create_employee,
    "get_employee": get_employee,
    "get_all_employees": get_all_employees,
    "update_employee": update_employee,
    "delete_employee": delete_employee,
    "search_by_name": search_by_name,
    "search_by_department": search_by_department,
    "search_by_city": search_by_city,
    "search_by_salary": search_by_salary,
    "count_employees": count_employees,
    "highest_salary": highest_salary,
    "search_department_salary": search_department_salary,
}


def _get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        raise RuntimeError(
            "Set OPENAI_API_KEY in the environment or Streamlit secrets."
        )
    return api_key


def ask_agent(question):
    """Answer a request and run relevant employee database operations."""
    if not question or not question.strip():
        raise ValueError("Please enter a request.")

    client = OpenAI(api_key=_get_api_key())
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant for an employee database. Use tools for database "
                "facts and changes. Never invent missing employee details; ask for all "
                "required details before changing a record. Never write SQL."
            ),
        },
        {"role": "user", "content": question.strip()},
    ]

    for _ in range(5):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=_TOOLS,
            tool_choice="auto",
        )
        message = response.choices[0].message
        if not message.tool_calls:
            return message.content or "The agent did not return a response."

        messages.append(message)
        for tool_call in message.tool_calls:
            function = _FUNCTIONS.get(tool_call.function.name)
            try:
                arguments = json.loads(tool_call.function.arguments)
                if function is None:
                    result = {"success": False, "message": "Unknown database operation."}
                else:
                    result = function(**arguments)
            except (TypeError, ValueError, json.JSONDecodeError) as error:
                result = {"success": False, "message": str(error)}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            })

    raise RuntimeError("The agent exceeded the maximum number of tool-call rounds.")


__all__ = ["ask_agent"]
