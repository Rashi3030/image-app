import streamlit as st
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
from datetime import datetime

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
db = client["moneyhive_bank"]
users_collection = db["users"]
transactions_collection = db["transactions"]
notifications_collection = db["notifications"]

# Helper Functions
def hash_password(password):
    """Hash a password for secure storage."""
    return pbkdf2_sha256.hash(password)

def verify_password(password, hashed):
    """Verify a password against its hash."""
    return pbkdf2_sha256.verify(password, hashed)

def register_user(username, password):
    """Register a new user."""
    if users_collection.find_one({"username": username}):
        return "Username already exists."
    hashed_password = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_password, "balance": 0.0})
    return "Registration successful!"

def authenticate_user(username, password):
    """Authenticate user credentials."""
    user = users_collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return user
    return None

def get_notifications():
    """Retrieve all notifications."""
    return notifications_collection.find().sort("timestamp", -1)

# Streamlit App
st.set_page_config(page_title="MoneyHive Bank", layout="wide")

# Header Section
st.markdown(
    """
    <style>
        .header {
            font-size: 32px;
            font-weight: bold;
            color: #0070c0;
            text-align: center;
            padding: 20px 0;
        }
        .subheader {
            font-size: 18px;
            color: #333333;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
    <div class="header">MONEYHIVE BANK</div>
    <div class="subheader">Your trusted partner for all financial needs</div>
    """,
    unsafe_allow_html=True,
)

# Sidebar Menu
menu = st.sidebar.radio("Navigation", ["Home", "Account", "Login", "Notifications", "Customer Service"])

# Home Page
if menu == "Home":
    st.subheader("Welcome to MoneyHive Bank")
    st.write("Explore our services and manage your finances with ease. Use the navigation menu to access your account, login, or contact customer service.")

# Account Registration
elif menu == "Account":
    st.subheader("Create a New Account")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    if st.button("Register"):
        result = register_user(username, password)
        st.success(result)

# Login Page
elif menu == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.success(f"Welcome back, {username}!")
            balance = users_collection.find_one({"username": username})["balance"]
            st.info(f"Your current balance is: ₹{balance}")
        else:
            st.error("Invalid username or password.")

# Notifications Page
elif menu == "Notifications":
    st.subheader("Notifications")
    st.write("Here are the latest updates and notifications:")
    notifications = get_notifications()
    for notification in notifications:
        st.write(f"- {notification['message']} (Date: {notification['timestamp']})")

# Customer Service
elif menu == "Customer Service":
    st.subheader("Contact Customer Service")
    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Email")
    message = st.text_area("Enter Your Message")
    if st.button("Submit"):
        st.success("Your message has been sent. We will get back to you shortly!")



