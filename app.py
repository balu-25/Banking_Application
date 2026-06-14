import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.db import create_tables,get_connection

from services.auth_service import (
register_user,
login_user,
login_admin
)

from services.transaction_service import (
deposit,
withdraw,
get_balance
)

from services.loan_service import (
apply_loan,
pay_loan
)

create_tables()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "userid" not in st.session_state:
    st.session_state.userid = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
st.title("🏦 Banking Management System")

menu=st.sidebar.selectbox(
"Menu",
["User Signup",
 "User Login",
 "Admin Login"]
)

# USER SIGNUP

if menu=="User Signup":

    st.header("User Registration")

    name=st.text_input("Name")
    phone=st.text_input("Phone")
    email=st.text_input("Email")
    userid=st.text_input("User ID")
    password=st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        register_user(
            name,
            phone,
            email,
            userid,
            password
        )

        st.success(
            "Account Created with ₹1000"
        )

# USER LOGIN

elif menu == "User Login":

    if not st.session_state.logged_in:

        userid = st.text_input("User ID")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(userid, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.userid = userid
                st.rerun()

            else:
                st.error("Invalid Credentials")

    else:

        userid = st.session_state.userid

        st.success(f"Logged in as {userid}")

        action = st.selectbox(
            "Select Action",
            [
                "Check Balance",
                "Deposit",
                "Withdraw",
                "Apply Loan",
                "Pay Loan"
            ]
        )

        if action == "Check Balance":

            st.subheader("Balance")

            st.write(
                f"₹ {get_balance(userid)}"
            )

        elif action == "Deposit":

            amount = st.number_input(
                "Amount",
                min_value=1.0
            )

            if st.button("Deposit"):

                deposit(userid, amount)

                st.success("Money Deposited")

                st.write(
                    "Updated Balance:",
                    get_balance(userid)
                )

        elif action == "Withdraw":

            amount = st.number_input(
                "Amount",
                min_value=1.0
            )

            if st.button("Withdraw"):

                if withdraw(userid, amount):

                    st.success("Money Withdrawn")

                    st.write(
                        "Updated Balance:",
                        get_balance(userid)
                    )

                else:

                    st.error(
                        "Insufficient Balance"
                    )

        elif action == "Apply Loan":

            loan_type = st.selectbox(
                "Loan Type",
                ["Home", "Car", "Education"]
            )

            amount = st.number_input(
                "Loan Amount",
                min_value=1000.0
            )

            interest = st.number_input(
                "Interest",
                min_value=1.0
            )

            duration = st.number_input(
                "Duration",
                min_value=1
            )

            if st.button("Apply"):

                apply_loan(
                    userid,
                    loan_type,
                    amount,
                    interest,
                    duration
                )

                st.success(
                    "Loan Applied Successfully"
                )

        elif action == "Pay Loan":
            from services.loan_service import (
                pay_loan,
                get_pending_loan
            )

            pending = get_pending_loan(userid)

            st.write(
                f"Pending Loan Amount: ₹{pending}"
            )

            amount = st.number_input(
                "Enter Payment",
                min_value=1.0
            )

            if st.button("Pay Loan"):

                if pay_loan(userid, amount):

                    st.success(
                        "Loan Payment Successful"
                    )

                    st.write(
                        "Remaining Loan:",
                        get_pending_loan(userid)
                    )

                    st.write(
                        "Updated Balance:",
                        get_balance(userid)
                    )

                else:

                    st.error(
                        "Payment Failed"
                    )

        st.divider()

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.userid = None

            st.rerun()
# ADMIN LOGIN

elif menu=="Admin Login":

    empid=st.text_input("Employee ID")

    password=st.text_input(
        "Password",
        type="password"
    )

    if st.button("Admin Login"):

        admin=login_admin(
            empid,
            password
        )

        if admin:

            st.success("Welcome Admin")

            conn=get_connection()

            st.subheader("Users")

            users=pd.read_sql(
            """
            SELECT
            name,
            phone,
            email,
            userid,
            balance
            FROM users
            """,
            conn
            )

            st.dataframe(users)

            st.subheader(
            "Transactions"
            )

            trans=pd.read_sql(
            """
            SELECT *
            FROM transactions
            """,
            conn
            )

            st.dataframe(trans)
            st.subheader("Loans")

            loan_df = pd.read_sql(
            """
            SELECT *
            FROM loans
            """,
            conn
            )

            st.dataframe(loan_df)
            chart_df=pd.read_sql(
            """
            SELECT
            function,
            COUNT(*) as total
            FROM transactions
            GROUP BY function
            """,
            conn
            )

            if len(chart_df)>0:

                fig, ax = plt.subplots(figsize=(6, 6))

                ax.pie(
                    chart_df["total"],
                    labels=chart_df["function"],
                    autopct="%1.1f%%",
                    startangle=90
                )

                ax.set_title("Transactions Distribution")

                # 👇 MOVE legend OUTSIDE chart
                ax.legend(
                    chart_df["function"],
                    title="Transaction Types",
                    loc="center left",
                    bbox_to_anchor=(1, 0.5)
                )

                plt.tight_layout()

                st.pyplot(fig)

            conn.close()

        else:
            st.error("Invalid Login")