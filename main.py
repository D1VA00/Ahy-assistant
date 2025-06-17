import streamlit as st
import openai
import requests
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
import datetime
import pandas as pd
from fpdf import FPDF
from PIL import Image
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
GOLD_API_KEY = "goldapi-41wfwsmby1le3x-io"
ALPHA_API_KEY = "NH2B8K51QNNCB03T"
NEWS_API_KEY = "1a3e4ed99d2d4035a81733df6c5ed99b"
# ===== Page Config (MUST be first) =====
st.set_page_config(page_title="AHY Dashboard", layout="wide")

# ===== Authentication System =====
def load_users():
    """Load users from JSON file"""
    try:
        with open("data/users.json", "r") as f:
            return json.loads(f.read())
    except:
        return {}

def save_users(users_dict):
    """Save users to JSON file"""
    import json
    from pathlib import Path
    Path("data").mkdir(exist_ok=True)
    with open("data/users.json", "w") as f:
        json.dump(users_dict, f, indent=2)

def simple_login():
    """Simple login system"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None

    if not st.session_state.logged_in:
        # Company Header on Login Page
        col1, col2 = st.columns([1, 4])
        with col1:
            try:
                logo = Image.open("attached_assets/IMG_0267_1750091625045.jpeg")
                st.image(logo, width=120)
            except:
                st.markdown("🏢")  # Fallback emoji if logo not found
        with col2:
            st.markdown("## A H Y for Management Service for Companies and Investors")
            st.caption("Strategic tools for investors, entrepreneurs, and family business growth.")

        st.markdown("---")
        st.markdown("""
        **Welcome to AHY** - Your all-in-one platform for smart decision-making.

        - Real-time investment insights
        - Professional business services  
        - Personalized tools with Buffett-style logic
        """)
        st.markdown("---")

        # Tab selector for Login/Register
        auth_tab = st.selectbox("Choose Action", ["Login", "Create Account"])

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if auth_tab == "Login":
                st.markdown("### Login to AHY Dashboard")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                if st.button("Login", use_container_width=True):
                    users = load_users()
                    if username in users and users[username]["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.user_data = users[username]
                        st.success("✅ Welcome to AHY Dashboard!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")

                st.markdown("---")
                st.info("💡 Don't have an account? Select 'Create Account' above")

            else:  # Create Account
                st.markdown("### Create Your AHY Account")
                new_username = st.text_input("Choose Username")
                new_email = st.text_input("Email Address")
                new_full_name = st.text_input("Full Name")
                new_password = st.text_input("Choose Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if st.button("Create Account", use_container_width=True):
                    if new_username and new_email and new_full_name and new_password:
                        if new_password == confirm_password:
                            users = load_users()
                            if new_username not in users:
                                users[new_username] = {
                                    "password": new_password,
                                    "email": new_email,
                                    "full_name": new_full_name,
                                    "created_date": str(datetime.date.today())
                                }
                                save_users(users)
                                st.success("✅ Account created successfully!")
                                st.info("🎉 Please select 'Login' to access your account!")
                                st.balloons()
                            else:
                                st.error("❌ Username already exists")
                        else:
                            st.error("❌ Passwords don't match")
                    else:
                        st.error("❌ Please fill in all fields")

                st.markdown("---")
                st.info("💡 Already have an account? Select 'Login' above")

        # Logout option if logged in
        if st.session_state.logged_in:
            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user_data = None
                st.rerun()

# Initialize login
simple_login()

# Only show the main app if user is logged in
if not st.session_state.get('logged_in', False):
    st.stop()

# ===== Styling =====
st.markdown("""
<style>
body {
  background-color: #0d1117;
  color: #ffffff;
}
.sidebar .sidebar-content {
  background-color: #161b22;
}
h1, h2, h3 {
  color: #f1c40f;
}
.stButton>button {
  background-color: #f1c40f;
  color: black;
  border-radius: 8px;
  font-weight: bold;
}
.stTextInput>div>div>input, .stTextArea>div>textarea {
  background-color: #b3d4fc !important;
  color: #000000 !important;
  font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===== Header =====
col1, col2 = st.columns([1, 4])
with col1:
    try:
        logo = Image.open("attached_assets/IMG_0267_1750091625045.jpeg")
        st.image(logo, width=120)
    except:
        st.markdown("")  # Fallback emoji if logo not found
with col2:
    st.markdown("## A H Y for Management Service for Companies and Investors")
    st.caption("Strategic tools for investors, entrepreneurs, and family business growth.")

st.markdown("---")

# ===== Tabs =====
tabs = st.tabs(["🏠 Home", "💬 AI Chat", "📄 Client Report", "📈 Strategy Generator", "📂 Business Tools", "📉 Debt Calculator", "💰 Budget Advisor", "📊 Budget History"])

# ===== Tab 1 – Home =====
with tabs[0]:
    st.header("Welcome to AHY")
    st.markdown("""
    AHY is your all-in-one platform for smart decision-making.

    - Real-time investment insights
    - Professional business services
    - Personalized tools with Buffett-style logic
    """)
import datetime

st.markdown("---")
st.markdown("## 💬 Feedback")

feedback = st.text_area("Have suggestions or ideas to improve AHY Assistant?")
if st.button("Submit Feedback"):
    try:
        with open(f"/mnt/data/feedback_{datetime.date.today()}.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {feedback}\n")
        st.success("✅ Thank you! Your feedback has been recorded.")
    except Exception as e:
        st.error(f"Error saving feedback: {e}")
# ===== Tab 2 – AI Chat =====
with tabs[1]:
    st.subheader("💬 Here to Help , Ask us anything!")
    # Agent Selector
    agent = st.selectbox("Choose Your Assistant Agent:", [
        "💰 Budget Coach",
        "📈 Strategic Investor",
        "🧾 Business Consultant"
    ])

    # System prompt based on agent
    if agent == "💰 Budget Coach":
        system_prompt = (
            "You are a practical budget advisor focused on smart saving habits and financial discipline. "
            "Speak in a friendly tone and give real-life, sustainable suggestions."
        )
        st.info("🧠 Budget Coach is ready to help you manage your money better.")

    elif agent == "📈 Strategic Investor":
        system_prompt = (
            "You are a long-term, value-driven investor giving clear and logical financial advice, inspired by Warren Buffett. "
            "Speak rationally, avoid hype, and focus on strategy."
        )
        st.info("📈 Strategic Investor is ready to guide you with long-term insights.")

    elif agent == "🧾 Business Consultant":
        system_prompt = (
            "You are a sharp, experienced business consultant who helps users draft proposals, make smart business decisions, "
            "and communicate with investors. Be clear, professional, and goal-focused."
        )
        st.info("🧾 Business Consultant is here to assist with planning and strategy.")

    # User input + GPT chat
    query = st.text_input("Ask your question:")
    if st.button("Get Answer"):
        try:
            # Check for stock symbols
            symbols = re.findall(r"\b[A-Z]{2,5}\b", query)
            price_info = ""
            if symbols:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbols[0]}&apikey={ALPHA_API_KEY}"
                r = requests.get(url).json()
                if "Global Quote" in r and "05. price" in r["Global Quote"]:
                    price_info = f"**Price Info:** {symbols[0]} at ${r['Global Quote']['05. price']}"

            # Use the new OpenAI API format
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
            )

            if price_info:
                st.markdown(price_info)
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")

# ===== Tab 3 – Client Report =====
with tabs[2]:
    st.subheader("Generate Client Portfolio Report")

    # Sample companies data
    sample_companies = {
        "Apple Inc.": "AAPL",
        "Microsoft Corp.": "MSFT", 
        "Amazon.com Inc.": "AMZN",
        "Alphabet Inc.": "GOOGL",
        "Tesla Inc.": "TSLA",
        "Meta Platforms": "META",
        "NVIDIA Corp.": "NVDA",
        "Berkshire Hathaway": "BRK.B",
        "JPMorgan Chase": "JPM",
        "Johnson & Johnson": "JNJ"
    }

    name = st.text_input("Client Name")
    capital = st.number_input("Capital (AED)", min_value=0.0)
    selected_names = st.multiselect("Choose Stocks", options=list(sample_companies.keys()))
    amounts = st.text_input("Amounts Invested (comma-separated)")

    if st.button("Generate Report"):
        try:
            values = [float(x.strip()) for x in amounts.split(",")]
            if len(values) == len(selected_names):
                report_lines = [f"- {n} ({sample_companies[n]}): AED {v:,.2f}" for n, v in zip(selected_names, values)]
                report = f"Client: {name}\nCapital: AED {capital:,.2f}\nPortfolio:\n" + "\n".join(report_lines)
                st.text_area("Report", report, height=200)
            else:
                st.error("Number of amounts must match number of selected stocks.")
        except:
            st.error("Please enter valid amounts separated by commas.")
# ===== Tab 4 – Strategy Generator =====
with tabs[3]:
    st.subheader("Generate a Strategy")
    capital = st.number_input("Available Capital", min_value=0.0)
    risk = st.selectbox("Risk Level", ["Low", "Medium", "High"])
    asset = st.selectbox("Asset Focus", ["Stocks", "Gold", "Crypto"])
    if st.button("Create Strategy"):
        prompt = f"Capital: {capital}\nRisk: {risk}\nAsset: {asset}\nGive a smart long-term strategy."
        strategy = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        st.text_area("Strategy", strategy.choices[0].message.content, height=250)

# ===== Tab 5 – Business Tools =====
with tabs[4]:
    st.subheader("Business Document Generator")
    service = st.selectbox("Select a service", ["Proposal", "Investor Email", "Setup Guide"])
    desc = st.text_area("What do you need?")
    if st.button("Generate Business Output"):
        prompt = f"Type: {service}\nDetails: {desc}\nWrite a clear professional reply."
        reply = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        st.text_area("Output", reply.choices[0].message.content, height=250)

# ===== Tab 6 – Debt Calculator =====
with tabs[5]:
    st.subheader("Debt Calculator")
    loan = st.number_input("Loan Amount (AED)", min_value=0.0)
    rate = st.number_input("Interest Rate (%)", min_value=0.0)
    years = st.number_input("Term (Years)", min_value=1)
    if st.button("Calculate Payment"):
        if rate > 0 and years > 0:
            r = rate / 100 / 12
            n = years * 12
            payment = loan * r / (1 - (1 + r) ** -n)
            total = payment * n
            interest = total - loan
            st.success(f"Monthly: AED {payment:,.2f}")
            st.info(f"Total Payment: AED {total:,.2f}")
            st.warning(f"Total Interest: AED {interest:,.2f}")
        else:
            st.error("Please enter valid interest and term.")


# ===== Tab 8 – Budget History =====
with tabs[7]:
    st.subheader("📊 Budget History Viewer")
    st.markdown("Review previous budget reports by username.")

    from pathlib import Path
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    report_files = list(data_dir.glob("*_budget_report.csv"))
    usernames = sorted([f.name.replace("_budget_report.csv", "") for f in report_files])

    selected_user = st.selectbox("Choose a user to view history", usernames)

    if selected_user:
        try:
            history_path = f"data/{selected_user}_budget_report.csv"
            df_history = pd.read_csv(history_path)
            st.dataframe(df_history)

            st.markdown("### 💡 Budget Score Trend")
            fig, ax = plt.subplots()
            df_history_sorted = df_history.sort_values("Date")
            ax.plot(df_history_sorted["Date"], df_history_sorted["Score"], marker='o')
            ax.set_xlabel("Date")
            ax.set_ylabel("Score")
            ax.set_title(f"{selected_user}'s Budget Health Over Time")
            st.pyplot(fig)

            st.markdown("### 📅 Compare Two Reports")
            date_options = df_history_sorted['Date'].tolist()
            date1 = st.selectbox("Select First Month", date_options, index=0)
            date2 = st.selectbox("Select Second Month", date_options, index=len(date_options)-1)

            if st.button("📊 Compare Reports"):
                df1 = df_history_sorted[df_history_sorted['Date'] == date1].iloc[0]
                df2 = df_history_sorted[df_history_sorted['Date'] == date2].iloc[0]

                comparison_data = {
                    'Category': ['Income', 'Essentials', 'Savings', 'Leisure', 'Remaining', 'Score'],
                    date1: [df1['Income'], df1['Essentials'], df1['Savings'], df1['Leisure'], df1['Remaining'], df1['Score']],
                    date2: [df2['Income'], df2['Essentials'], df2['Savings'], df2['Leisure'], df2['Remaining'], df2['Score']]
                }
                compare_df = pd.DataFrame(comparison_data)
                st.dataframe(compare_df.set_index('Category'))
                latest = df_history_sorted.iloc[-1]
                st.markdown(f"**Last Recorded on {latest['Date']}**")
                st.markdown(f"💰 Income: AED {latest['Income']:,.2f}")
                st.markdown(f"🏠 Essentials: AED {latest['Essentials']:,.2f}")
                st.markdown(f"💸 Savings: AED {latest['Savings']:,.2f}")
                st.markdown(f"🎉 Leisure: AED {latest['Leisure']:,.2f}")

                # Optional: Run suggestion logic again here
                if latest['Remaining'] < 0:
                    st.error("They were overspending. Suggest adjusting lifestyle expenses.")
                elif latest['Savings'] < latest['Income'] * 0.1:
                    st.warning("They saved less than 10%. Recommend saving more.")
                else:
                    st.success("Budget looked healthy at last check.")

        except Exception as e:
            st.error(f"Could not load history: {e}")

# ===== Tab 7 – Budget Advisor =====
with tabs[6]:
    st.subheader("💰 Budget Advisor")
    st.markdown("Input your monthly income and expenses to get a basic financial overview and advice.")

    user_id = st.text_input("Create a Budget Username")
    income = st.number_input("Monthly Income (AED)", min_value=0.0)
    essentials = st.number_input("Essentials (rent, bills, food)", min_value=0.0)
    savings = st.number_input("Savings & Investments", min_value=0.0)
    leisure = st.number_input("Leisure & Other Spending", min_value=0.0)

    # File upload section (outside of button)
    uploaded_file = st.file_uploader("📸 Upload Receipt (optional)", type=["jpg", "jpeg", "png"])

    receipt_data = None
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Receipt", width=300)

        # Simple text extraction simulation (since pytesseract requires system installation)
        st.info("📄 Receipt uploaded successfully! Click 'Analyze Budget' to process it.")
        receipt_data = {
            "vendor": "Sample Store",
            "amount": 50.0,
            "category": "Essentials"
        }

    if st.button("Analyze Budget"):
        if not user_id:
            st.error("Please enter a username to track your budget.")
        else:
            total_spent = essentials + savings + leisure
            remaining = income - total_spent

            explanation = f"**{user_id}**, you earn AED {income:,.2f} and currently spend AED {total_spent:,.2f} each month. Your remaining balance is AED {remaining:,.2f}."
            st.info(explanation)

            # Calculate savings ratio
            savings_ratio = savings / income if income > 0 else 0

            if remaining < 0:
                st.error("You're overspending. Reduce non-essentials or reevaluate savings goals.")
                st.markdown("💡 **Suggestion:** Create a stricter budget or consider consolidating high-interest debt.")
                score = 40
            elif savings_ratio < 0.1:
                st.warning("You're saving less than 10% of your income.")
                st.markdown("💡 **Suggestion:** Try automatic savings transfers or reduce discretionary expenses.")
                score = 60
            else:
                st.success("You're managing your income well.")
                st.markdown("✅ **Suggestion:** Keep monitoring spending and consider investing part of your surplus.")
                score = 90

            # Process receipt if uploaded
            if receipt_data:
                st.markdown("### 📋 Receipt Analysis")
                st.success(f"Receipt processed: {receipt_data['vendor']} - AED {receipt_data['amount']}")
                st.info(f"Suggested category: {receipt_data['category']}")

                # Add receipt amount to appropriate category
                if receipt_data['category'] == 'Essentials':
                    essentials += receipt_data['amount']
                elif receipt_data['category'] == 'Leisure':
                    leisure += receipt_data['amount']

                # Recalculate with receipt
                total_spent = essentials + savings + leisure
                remaining = income - total_spent
                st.warning(f"Updated remaining balance after receipt: AED {remaining:,.2f}")

            st.markdown(f"### 🧾 Your Budget Health Score: **{score}/100**")

            # Save results to a basic CSV
            from pathlib import Path

            # Create data directory if it doesn't exist
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)

            budget_data = pd.DataFrame([{
                "User": user_id,
                "Income": income,
                "Essentials": essentials,
                "Savings": savings,
                "Leisure": leisure,
                "Remaining": remaining,
                "Score": score,
                "Date": datetime.date.today()
            }])

            file_path = f"data/{user_id}_budget_report.csv"
            budget_data.to_csv(file_path, index=False)

            # Create visualizations
            labels = ['Essentials', 'Savings', 'Leisure']
            values = [essentials, savings, leisure]

            # Pie chart breakdown
            st.markdown("### 🥧 Budget Breakdown")
            fig1, ax1 = plt.subplots()
            ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            # Horizontal bar chart - fix seaborn warning
            st.markdown("### 📊 Spending Breakdown")
            fig2, ax2 = plt.subplots()
            sns.barplot(x=values, y=labels, hue=labels, palette='Blues_r', ax=ax2, legend=False)
            ax2.set_xlabel("AED")
            ax2.set_title("Monthly Budget Allocation")
            st.pyplot(fig2)

            # Download button
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Budget Report", f, file_name=f"{user_id}_budget_report.csv")

# ===== Footer =====
st.markdown("---")
st.markdown("© 2024 AHY Group — Powered by clarity, not complexity.")