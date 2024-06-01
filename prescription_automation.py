import imaplib
import email
from email.header import decode_header
import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re # Import the re module for regular expressions

# Define log function for logging
def log(message):
    with open('/home/ubuntu/automated-prescription-system/cron_log.txt', 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - {message}\n')

# Email credentials
email_user = 'your email'
email_pass = 'your app password'

# Fetch emails function
def fetch_emails():
    log('Starting to fetch emails')
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_user, email_pass)
        mail.select('inbox')

        status, messages = mail.search(None, '(FROM "flow@shopify.com")')
        email_list = messages[0].split()
        emails = []

        for num in email_list:
            status, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            emails.append(msg)
        mail.logout()
        log(f'Fetched {len(emails)} emails')
        return emails
    except Exception as e:
        log(f'Error fetching emails: {str(e)}')
        return []

# Extract prescription link function
def extract_prescription_link(email_message):
    log('Extracting prescription link')
    try:
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload(decode=True).decode()
                    soup = BeautifulSoup(body, 'html.parser')
                    link = soup.find('a', href=True)
                    if link:
                        log(f'Found link: {link["href"]}')
                        return link['href']
        else:
            body = email_message.get_payload(decode=True).decode()
            soup = BeautifulSoup(body, 'html.parser')
            link = soup.find('a', href=True)
            if link:
                log(f'Found link: {link["href"]}')
                return link['href']
        log('No link found')
        return None
    except Exception as e:
        log(f'Error extracting link: {str(e)}')
        return None

# Create AWS S3 URL from the extracted link
def create_aws_url(prescription_link):
    try:
        base_s3_url = "https://erwdev.s3.amazonaws.com/chambora/prescriptions"
        date_part = re.search(r'/prescriptions/(\d{4}-\d{2}-\d{2})/', prescription_link).group(1)  # Extract the date part from the link
        file_name = prescription_link.split('/')[-1]
        aws_url = f"{base_s3_url}/{date_part}/{file_name}"
        log(f'Created AWS URL: {aws_url}')
        return aws_url
    except Exception as e:
        log(f'Error creating AWS URL: {str(e)}')
        return None

# Send email with new URL function
def send_email_with_aws_url(to_email, subject, body, aws_url):
    log(f'Sending email to {to_email} with AWS URL {aws_url}')
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = subject

        body = f"{body}\n\nLens Advisor AWS Media Link: {aws_url.replace('?auth_url=chambora/', '/')}"  # Replace the part of the URL
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            text = msg.as_string()
            server.sendmail(email_user, to_email, text)
        log('Email sent successfully')
    except Exception as e:
        log(f'Error sending email: {str(e)}')

def main():
    log('Script execution started')
    emails = fetch_emails()
    for email_message in emails:
        order_number = decode_header(email_message['Subject'])[0][0]
        if isinstance(order_number, bytes):
            order_number = order_number.decode()

        link = extract_prescription_link(email_message)
        if link:
            aws_url = create_aws_url(link)
            if aws_url:
                send_email_with_aws_url('suplier email', f'Order {order_number}', 'Please find the prescription attached.', aws_url)
    log('Script execution completed')

if __name__ == "__main__":
    main()
