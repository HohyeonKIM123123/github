# Email notification system
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import os

class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email = os.getenv('EMAIL_ADDRESS')
        self.password = os.getenv('EMAIL_PASSWORD')
    
    def send_overdue_notification(self, member_email: str, member_name: str, overdue_books: List[Dict]) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = member_email
            msg['Subject'] = "도서관 연체 도서 알림"
            
            body = f"안녕하세요 {member_name}님,\n\n"
            body += "다음 도서들이 연체되었습니다:\n\n"
            
            for book in overdue_books:
                body += f"- {book['title']} (대출일: {book['loan_date']}, 반납예정일: {book['due_date']})\n"
            
            body += "\n빠른 시일 내에 반납해 주시기 바랍니다.\n\n감사합니다."
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"이메일 전송 실패: {e}")
            return False
    
    def send_bulk_notifications(self, overdue_data: List[Dict]) -> int:
        success_count = 0
        for member_data in overdue_data:
            if self.send_overdue_notification(
                member_data['email'], 
                member_data['name'], 
                member_data['books']
            ):
                success_count += 1
        return success_count