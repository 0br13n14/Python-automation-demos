#importing required libraries
import smtplib
from email.message import EmailMessage
import os 
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

msg = EmailMessage()
msg["Subject"] = "Automated Email Sender Testing"
msg["From"] = email_address
msg["To"] = "@gmail.com"
msg.set_content("Hi, this is a test email sent from my Python script. The purpose of it is to send emails automatically wihout much manual work")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(email_address, email_password)
    smtp.send_message(msg)

print("Email sent successfully!")
