import csv
import smtplib
from email.message import EmailMessage
import os 
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


# Get the folder where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build path to any file in the same folder
CUSTOMER_CSV = os.path.join(SCRIPT_DIR, "bulk_testing.csv")

with open(CUSTOMER_CSV, "r") as file:

    reader = csv.DictReader(file)
    for row in reader:
        msg = EmailMessage()
        msg["Subject"] = "Automated Email Sender Testing"
        msg["From"] = email_address
        msg["To"] = row["email"]
        msg.set_content(f"Dear {row["name"]}: \n please be aware that you have a due balance of {row["amount"]}")

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(email_address, email_password)
            smtp.send_message(msg)

    print("Email sent successfully!")
