import imaplib
import email
from email.header import decode_header
import requests
import os
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup

# Configuration
imap_host = 'imap.gmail.com'
smtp_host = 'smtp.gmail.com'
smtp_port = 587
email_user = 'Tom@v2ogroup.com'
email_pass = 'T00124472H!?#'
supplier_email = 'info@spektaclesolutions.co.uk'

lensadvizor_token = 'la_f540161C1fca6E590dBD42aa7125f1116Ea7cB'
lensadvizor_shop = 'chambora.myshopify.com'

# Function to fetch emails
def fetch_emails():
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    status, messages = mail.search(None, '(FROM "flow" OR FROM "order automator")')
    messages = messages[0].split()

    email_data = []
    for mail_id in messages:
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        email_data.append(msg)

    mail.logout()
    return email_data

# Function to extract the LensAdvisor link from email
def extract_link(email_body):
    for part in email_body.walk():
        if part.get_content_type() == "text/html":
            body = part.get_payload(decode=True).decode()
            soup = BeautifulSoup(body, "html.parser")
            for a in soup.find_all('a', href=True):
                if 'lensadvizor' in a['href']:
                    return a['href']
    return None

# Function to download media file from LensAdvisor
def download_media_file(link, order_number, order_date):
    url = f"https://api.lensadvizor.com/v1/prescriptions?shop={lensadvizor_shop}"
    headers = {
        "X-LensAdvizor-Access-Token": lensadvizor_token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        prescriptions = response.json()
        for prescription in prescriptions:
            if prescription['link'] == link:
                media_url = prescription['media_url']
                file_extension = media_url.split('.')[-1]
                file_name = f"Order-{order_number}-{order_date}.{file_extension}"
                file_path = os.path.join("downloads", file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                media_response = requests.get(media_url)
                with open(file_path, 'wb') as f:
                    f.write(media_response.content)
                return file_path
    return None

# Function to send email with attachment
def send_email_with_attachment(subject, body, attachment_path):
    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = supplier_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)

# Main function to orchestrate the process
def main():
    emails = fetch_emails()
    for msg in emails:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition:
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    order_number = subject.split('#')[1]
                    order_date = msg["Date"][:16].replace(" ", "-")
                    link = extract_link(msg)
                    if link:
                        attachment_path = download_media_file(link, order_number, order_date)
                        if attachment_path:
                            email_subject = f'Order #{order_number} Prescription'
                            email_body = 'Please find the attached prescription.'
                            send_email_with_attachment(email_subject, email_body, attachment_path)

if __name__ == "__main__":
    main()
