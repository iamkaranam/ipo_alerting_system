import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List


class Mailer:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(
        self,
        recipients: List[str],
        subject: str,
        body: str
    ):
        if not recipients:
            raise ValueError("Recipient list cannot be empty")

        # Create email
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(
                    self.sender_email,
                    recipients,
                    message.as_string()
                )
            print("Email sent successfully!")

        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")
