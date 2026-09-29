import streamlit as st

from database import (
    create_table,
    get_all_employees
)

from agent import ask_agent


create_table()


st.set_page_config(
    page_title="AI Employee Database Agent",
    page_icon="🤖",
    layout="wide"
)


st.title(
    "🤖 AI Employee Database Agent"
)

st.caption(
    "OpenAI + Function Calling + SQLite + Streamlit"
)


tab1, tab2, tab3 = st.tabs(
    [
        "🤖 AI Agent",
        "📊 Employees",
        "ℹ️ About"
    ]
)


# ==================================================
# AI AGENT
# ==================================================

with tab1:

    st.header(
        "Ask the AI Agent"
    )

    st.write(
        """
        You can ask the agent to create, read,
        update, delete, or search employees.
        """
    )


    question = st.text_area(

        "Enter your request",

        placeholder="""
Examples:

Show all employees.

How many employees are there?

Find employees from IT.

Find employees from Kolkata.

Who has the highest salary?

Find employees earning between 40000 and 60000.

Add Rahul as an IT employee with salary 55000.

Update employee 1 salary to 65000.

Delete employee 3.
"""
    )


    if st.button(
        "🚀 Execute",
        type="primary"
    ):

        if not question.strip():

            st.warning(
                "Please enter a request."
            )

        else:

            with st.spinner(
                "AI Agent is working..."
            ):

                try:

                    answer = ask_agent(
                        question
                    )

                    st.success(
                        "Agent completed the request."
                    )

                    st.markdown(
                        "### AI Response"
                    )

                    st.write(answer)

                except Exception as error:

                    st.error(
                        f"Error: {error}"
                    )


# ==================================================
# EMPLOYEES
# ==================================================

with tab2:

    st.header(
        "Employee Database"
    )


    employees = get_all_employees()


    if employees:

        st.dataframe(
            employees,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No employees found."
        )


    if st.button(
        "🔄 Refresh"
    ):

        st.rerun()


# ==================================================
# ABOUT
# ==================================================

with tab3:

    st.header(
        "About This Application"
    )

    st.write(
        """
        This application demonstrates an AI Agent
        that can interact with a SQLite database.

        Technologies:

        • Python
        • OpenAI
        • Function Calling
        • SQLite
        • Streamlit

        The AI does not directly execute SQL.

        Instead:

        User → OpenAI Agent → Python Tool → SQLite

        The database operation result is then
        returned to the AI Agent.
        """
    )
