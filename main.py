"""
A Tkinter desktop app for sending a single email through Gmail SMTP.
The user fills in From, App Password, To, Subject, Body, clicks Send,
and the app reports each step (connecting, authenticating, sending).
"""
import tkinter as tk
import smtplib
from email.message import EmailMessage
from tkinter import ttk

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
        self.root.minsize (200,200)

        self.from_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.to_var = tk.StringVar()
        self.subject_var = tk.StringVar()

    def build_ui(self):
        # build_ui(self)
        #   - Title label at the top
        title = tk.Label(self.root, text = "EmailSenderApp",)
        title.pack(pady=(10,4))

        #form
        frame = tk.Frame(self.root, padx = 20, pady = 10)
        frame.pack(fill = tk.BOTH, expand = True)

        # from_var
        tk.Label(frame, text = "From(Your Gmail):",).grid(row = 0, column =0, sticky="w",pady = (0,4))
        from_var = tk.Entry(frame, textvariable = self.from_var, width = 50)
        from_var.grid(row = 0, column =1,sticky="ew", pady = (0,4))

        # password
        tk.Label(frame, text="Password:", ).grid(row=1, column=0, sticky="w",pady = (0,4))
        password = ttk.Entry(frame, textvariable = self.password_var, show="\u2022")
        password.grid(row=1, column=1, sticky="ew", width = 50)
        tk.Label(frame, text="(16-digit Gmail App Password \u2014 see Setup)",
                 fg="#666666", font=("Arial", 8)).grid(
            row=2, column=1, sticky="w", pady=(0, 8))

        # to_var
        tk.Label(frame, text="To:", ).grid(row=3, column=0, sticky="w", pady=(0,4))
        to_var = ttk.Entry(frame, textvariable = self.to_var, width =50)
        to_var.grid(row=0, column=0, sticky="ew", pady = (0,4))

        #subject
        tk.Label(frame, text="Subject:", ).grid(row=4, column=0, sticky="w",pady=(0,4))
        subject = ttk.Entry(frame,textvariable = self.subject_var, width =50)
        subject.grid(row=4, column=1, sticky="ew", pady=(0, 4))

        # body
        tk.Label(frame, text="Body:", ).grid(row=5, column=0, sticky="nw", pady=(8, 4))
        body_text = ttk.Entry(frame, textvariable=self.subject_var, width=50)
        body_text.grid(row=5, column=1, sticky="nsew", pady=(8, 4))
