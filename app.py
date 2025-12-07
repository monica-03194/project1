# app.py
import streamlit as st
from utils.auth import register_user, authenticate_user
from utils.queries import insert_query, get_queries, close_query
from utils.analytics import add_resolution_hours, get_trend_df, get_support_load

def show_login_page():
    st.title("🔐 Client Query Management System")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    # Register tab
    with tab_register:
        st.subheader("Create an account")

        reg_user = st.text_input("Username", key="reg_user")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        reg_mobile = st.text_input("Mobile Number", key="reg_mobile")
        reg_role = st.selectbox("Role", ["Client", "Support"], key="reg_role")

        if st.button("Register"):
            if not reg_user or not reg_pass or not reg_mobile:
                st.warning("All fields are required.")
            else:
                ok, msg = register_user(reg_user, reg_pass, reg_role, reg_mobile)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    # Login tab
    with tab_login:
        st.subheader("Login")

        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login Now"):
            u = authenticate_user(login_user, login_pass)
            if u:
                st.success("Login successful.")
                st.session_state.logged_in = True
                st.session_state.username = u["username"]
                st.session_state.role = u["role"]
                st.session_state.mobile = u["mobile_number"]
                st.session_state.current_page = "dashboard"
            else:
                st.error("Invalid credentials.")

def show_client_page():
    st.title("📨 Client — Submit Query")

    with st.form("client_form"):
        email = st.text_input("Your Email")
        mobile = st.text_input("Your Mobile", value=st.session_state.get("mobile", ""))
        heading = st.text_input("Query Heading")
        desc = st.text_area("Query Description")

        submit = st.form_submit_button("Submit")

        if submit:
            if email and mobile and heading and desc:
                insert_query(email, mobile, heading, desc)
                st.success("Query submitted successfully.")
            else:
                st.warning("All fields are required.")

    st.markdown("---")
    st.subheader("📋 All Queries")
    df_all = get_queries()
    st.dataframe(df_all)

    st.markdown("---")
    st.subheader("📌 My Queries (by Mobile)")
    if not df_all.empty:
        my_df = df_all[df_all["client_mobile"] == st.session_state.get("mobile")]
        if not my_df.empty:
            st.dataframe(my_df)
        else:
            st.info("You have not submitted any queries yet.")

def show_support_page():
    st.title("🛠 Support Dashboard")

    status_filter = st.selectbox("Filter by Status", ["All", "Open", "Closed"])
    df = get_queries(status_filter)

    if df.empty:
        st.info("No queries found.")
        return

    st.subheader("📋 Query Table")
    st.dataframe(df)

    # Support load metrics
    st.markdown("---")
    st.subheader("📈 Support Load")
    total, open_count, closed_count = get_support_load(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Queries", total)
    c2.metric("Open", open_count)
    c3.metric("Closed", closed_count)

    # Trend
    st.markdown("---")
    st.subheader("📅 Query Trend Over Time")
    trend_df = get_trend_df(df)
    if not trend_df.empty:
        st.line_chart(trend_df.set_index("date"))
    else:
        st.info("Not enough data for trends.")

    # Resolution Analysis
    st.markdown("---")
    st.subheader("⏱ Resolution Time Analysis")
    closed_df = add_resolution_hours(df)
    if not closed_df.empty:
        avg_res = closed_df["resolution_hours"].mean()
        fastest = closed_df["resolution_hours"].min()
        slowest = closed_df["resolution_hours"].max()

        r1, r2, r3 = st.columns(3)
        r1.metric("Avg (hrs)", f"{avg_res:.2f}")
        r2.metric("Fastest (hrs)", f"{fastest:.2f}")
        r3.metric("Slowest (hrs)", f"{slowest:.2f}")

        st.bar_chart(closed_df.set_index("query_id")["resolution_hours"])
    else:
        st.info("No closed queries to analyze resolution time.")

    # Close Query
    st.markdown("---")
    st.subheader("✅ Close an Open Query")
    open_df = df[df["status"] == "Open"]
    if open_df.empty:
        st.info("No open queries.")
        return

    qid = st.selectbox("Select Query ID", open_df["query_id"].tolist())
    if st.button("Close Selected Query"):
        if close_query(qid):
            st.success("Query closed. Reload dashboard to see updates.")
        else:
            st.error("Failed to close query.")

def main():
    st.set_page_config(page_title="Client Query System", page_icon="💬", layout="wide")

    # -------------------------------------------------
    # SAFE INITIALIZATION OF ALL SESSION VARIABLES
    # -------------------------------------------------
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"

    if "username" not in st.session_state:
        st.session_state.username = None

    if "role" not in st.session_state:
        st.session_state.role = None

    if "mobile" not in st.session_state:
        st.session_state.mobile = None
    # -------------------------------------------------

    # SIDEBAR
    with st.sidebar:
        st.header("Navigation")

        if st.session_state.logged_in:
            st.write(f"👤 {st.session_state.username} ({st.session_state.role})")
            st.write(f"📱 {st.session_state.mobile}")

            if st.button("Logout"):
                st.session_state.clear()
                st.session_state.logged_in = False
                st.session_state.current_page = "login"
                return
        else:
            st.info("Please log in.")

    # MAIN PAGE ROUTING
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.role == "Client":
            show_client_page()
        elif st.session_state.role == "Support":
            show_support_page()
        else:
            st.error("Invalid role. Contact admin.")


if __name__ == "__main__":
    main()
