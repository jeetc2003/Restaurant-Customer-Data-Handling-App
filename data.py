import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime

# Page Config (mobile-optimized)
st.set_page_config(page_title="Customer Entry", layout="centered")

st.markdown("## 🙋‍♂️ Welcome to Indian Coffee House")
st.markdown("Fill in your details for offers, updates, and special events 🎉")


# Connect to Google Sheets
@st.cache_resource
def connect_to_gsheets():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file("creds.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("Customers")

    # Create worksheet if it doesn't exist
    try:
        worksheet = sheet.worksheet("Customers")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title="Customers", rows="1000", cols="8")
        worksheet.append_row(
            [
                "VisitingFrequency",
                "Name",
                "PhoneNumber",
                "DateOfVisit",
                "Birthday",
                "Anniversary",
                "SpecialDates",
                "Reviews",
            ]
        )

    return worksheet


worksheet = connect_to_gsheets()

# Form options
visit_freq = ["First Time", "Once In A While", "Frequent"]

# Customer Form
with st.form("Customer_Form"):
    visit_frequency = st.selectbox("🕒 Visiting Frequency*", options=visit_freq)
    name = st.text_input("👤 Name*", max_chars=50)
    phone_number = st.text_input(
        "📞 Phone Number*", max_chars=10, help="Enter 10-digit mobile number"
    )

    birthday = st.text_input(
        "🎂 Want to share your Birthday",
        placeholder="Would Celebrate to make memories together 🕺 💃.",
    )

    anniversary = st.text_input(
        "❤️‍🩹 Want to share your Anniversary",
        placeholder="A perfect spot to propose again💖.",
    )

    special_date = st.text_input(
        "📅 Other Special Dates", placeholder="Special days for offers"
    )
    reviews = st.text_area(
        "📝 Feedback or Review",
        placeholder="E.g., Loved the kebab! Mutton Tehari was awesome $",
    )

    submitted = st.form_submit_button("✅ Submit")

    if submitted:
        if not name or not phone_number:
            st.warning("⚠️ Please fill all required fields marked with *")
        elif len(phone_number) != 10 or not phone_number.isdigit():
            st.error("❌ Enter a valid 10-digit phone number")
        else:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_row = [
                visit_frequency,
                name,
                phone_number,
                now,
                birthday,
                anniversary,
                special_date,
                reviews,
            ]

            try:
                worksheet.append_row(new_row)
                st.success("🎉 Thank you! Your details have been saved.")
            except Exception as e:
                st.error("❌ Could not save your data.")
                st.exception(e)
