# Email notification and communication service
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import os
from abc import ABC, abstractmethod

class EmailConnector(ABC):
    """Abstract base class for email services."""
    
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        pass

class SMTPEmailConnector(EmailConnector):
    """SMTP-based email connector for sending emails."""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587, 
                 sender_email: str = None, sender_password: str = None):
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', 587))
        self.sender_email = sender_email or os.getenv('SENDER_EMAIL')
        self.sender_password = sender_password or os.getenv('SENDER_PASSWORD')
    
    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        """Send email via SMTP."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to
            msg['Subject'] = subject
            
            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, mime_type))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email send error: {str(e)}")
            return False

class EmailTemplates:
    """Pre-built email templates for common scenarios."""
    
    @staticmethod
    def welcome_email(user_name: str, verification_link: str) -> tuple[str, str]:
        subject = "Welcome to Jarvondis Smart Chat!"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Welcome, {user_name}!</h2>
                <p>Thanks for signing up for Jarvondis Smart Chat - your safety-first AI assistant.</p>
                <p>Please verify your email by clicking the link below:</p>
                <p><a href="{verification_link}" style="background-color: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
                <p>If you didn't sign up, please ignore this email.</p>
                <hr>
                <footer style="color: #999; font-size: 12px;">
                    <p>Jarvondis Smart Chat - Advanced AI for Everyone</p>
                </footer>
            </body>
        </html>
        """
        return subject, body
    
    @staticmethod
    def password_reset_email(user_name: str, reset_link: str) -> tuple[str, str]:
        subject = "Reset Your Jarvondis Password"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Password Reset Request</h2>
                <p>Hi {user_name},</p>
                <p>We received a request to reset your password. Click the link below:</p>
                <p><a href="{reset_link}" style="background-color: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
                <p>This link expires in 1 hour.</p>
                <p>If you didn't request this, please ignore this email.</p>
                <hr>
                <footer style="color: #999; font-size: 12px;">
                    <p>Jarvondis Smart Chat - Advanced AI for Everyone</p>
                </footer>
            </body>
        </html>
        """
        return subject, body
    
    @staticmethod
    def skill_unlock_email(user_name: str, skill_name: str, skill_description: str) -> tuple[str, str]:
        subject = f"🎉 New Skill Unlocked: {skill_name}"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Congratulations, {user_name}!</h2>
                <p>You've unlocked a new skill: <strong>{skill_name}</strong></p>
                <p>{skill_description}</p>
                <p>Try it out now in your Jarvondis dashboard!</p>
                <hr>
                <footer style="color: #999; font-size: 12px;">
                    <p>Jarvondis Smart Chat - Advanced AI for Everyone</p>
                </footer>
            </body>
        </html>
        """
        return subject, body
