"""
A Tkinter desktop app for sending a single email through Gmail SMTP.
The user fills in From, App Password, To, Subject, Body, clicks Send,
and the app reports each step (connecting, authenticating, sending).
"""
import tkinter as tk
import smtplib
from email.message import EmailMessage
# from tkinter import ttk

# CONFIGURATION

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# PURE EMAIL FUNCTION

def send_email(sender, password, recipient, subject, body):
    """
    function takes user parameters and sends a request to start ttls encryption connection,
    authenticates and sends message
    """
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(msg)

# THE APP CLASS

class EmailSenderApp:
    """
        Initialize the main window, input variables and build the UI
    """
    def __init__(self, root):
        self.root = root
        self.root.title ("EmailSenderApp")

        self.from_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.to_var = tk.StringVar()
        self.subject_var = tk.StringVar()

        # self.build_ui()
