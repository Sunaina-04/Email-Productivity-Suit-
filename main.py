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
    Function takes user parameters and sends a request to start ttls encryption connection,
    authenticates and sends message
    send a plain text-email through Gmail SMTP. Raises on failure.
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
        self.root.geometry("700x550")
        self.root.minsize (200,200)

        self.from_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.to_var = tk.StringVar()
        self.subject_var = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        """Form labels for GUI"""
        #   - Title label at the top
        title = tk.Label(self.root, text = "EmailSenderApp",font=("Arial", 16, "bold"))
        title.pack(pady=(10,4))

        #form
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # from_var
        tk.Label(frame, text = "From(Your Gmail):",).grid(row = 0, column =0, sticky="w",pady = (0,4))
        from_var = tk.Entry(frame, textvariable = self.from_var, width = 50)
        from_var.grid(row = 0, column =1,sticky="ew", pady = (0,4))

        # password
        tk.Label(frame, text="Password:", ).grid(row=1, column=0, sticky="w",pady = (0,4))
        password = ttk.Entry(frame, textvariable = self.password_var,width = 50, show="\u2022",)
        password.grid(row=1, column=1, sticky="ew")
        tk.Label(frame, text="(16-digit Gmail App Password \u2014 see Setup)",
                 fg="#666666", font=("Arial", 8)).grid(
            row=2, column=1, sticky="w", pady=(0, 8))

        # to_var
        tk.Label(frame, text="To:", ).grid(row=3, column=0, sticky="w", pady=(0,4))
        to_var = ttk.Entry(frame, textvariable = self.to_var, width =50)
        to_var.grid(row=3, column=1, sticky="ew", pady = (0,4))

        #subject
        tk.Label(frame, text="Subject:", ).grid(row=4, column=0, sticky="w",pady=(0,4))
        subject = ttk.Entry(frame,textvariable = self.subject_var, width =50)
        subject.grid(row=4, column=1, sticky="ew", pady=(0, 4))

        # body
        tk.Label(frame, text="Body:", ).grid(row=5, column=0, sticky="nw", pady=(8, 4))
        self.body_text = tk.Text(frame, width = 50, height = 10, wrap = "word")
        self.body_text.grid(row = 5, column = 1, sticky = "nsew", pady=(8,4))

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5,weight = 1)

        # Buttons
        button_bar = tk.Frame(self.root)
        button_bar.pack(pady=10)

        tk.Button(button_bar, text= "\U0001F4E4 SEND EMAIL", command=self.on_send, font = ("Arial",13,"bold"), padx = 20, pady = 8).pack(side = "left", padx = 5)

        tk.Button(button_bar, text="\U0001F9F9 CLEAR", command=self.on_clear, font=("Arial", 13, "bold"), padx=20,
              pady=8).pack(side="left", padx=5)

        self.status_var = tk.StringVar(value = "Ready. Fill in the form and click Send.")
        tk.Label(self.root, textvariable=self.status_var, anchor = "w", bd=1, relief = "sunken", padx = 8, pady = 4).pack(fill= "x", side = "bottom")

    # Validations
    def validate(self):
        """Return an error message for the first invalid field in the form. If all is correct then send None"""
        if not self.from_var.get().strip():
            return "Please enter your Gmail address"
        if not self.password_var.get():
            return "Please enter your App Password."
        if not self.to_var.get().strip():
            return "Please enter a recipient."
        if not self.subject_var.get().strip():
            return "Please enter a subject."
        body = self.body_text.get("1.0", "end-1c").strip()
        if not body:
            return "Please enter a message body."
        return None

    def set_status(self, message):
        """Update the status bar AND forcefully repaint the GUI immediately"""
        self.status_var.set(message)
        self.root.update_idletasks()

    # Actions
    def on_send(self):
        """Validates and sends the email with updates"""
        # 1. Validate
        error = self.validate()
        if error :
            self.set_status(f"\u2717 {error}")
            return
        sender = self.from_var.get().strip()
        password = self.password_var.get()
        recipient = self.to_var.get().strip()
        subject = self.subject_var.get().strip()
        body = self.body_text.get("1.0", "end-1c").strip()

        # 2. Try sending the mail, with step-by-step updates
        try:
            self.set_status(f"Connecting to {SMTP_HOST}...")
            self.set_status("Authenticating and sending...")

            send_email(sender, password, recipient, subject, body)
            self.set_status(f"\u2713 Email sent to {recipient}")

        except smtplib.SMTPAuthenticationError:
            self.set_status("u\2717 Authentication failed: Check your Gmail address and App Password.(Reminder: No spaces.)")
        except smtplib.SMTPRecipientsRefused as e:
            self.set_status(f"\u2717 Recipient refused: {e} ")
        except smtplib.SMTPException as e:
            self.set_status(f"\u2717 Send failed: {e}")
        except Exception as e:
            self.set_status(f"\u2717 Error: {e}")

    def on_clear(self):
        """Reset every field"""
        self.from_var.set("")
        self.password_var.set("")
        self.to_var.set("")
        self.subject_var.set("")
        self.body_text.delete("1.0", "end")
        self.set_status("Form cleared.")

 # MAIN
def main():
    """ starts the main application loop"""
    root = tk.Tk()
    EmailSenderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()