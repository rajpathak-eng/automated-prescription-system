# Shopify Prescription Automation

This project automates the process of downloading and forwarding prescription files associated with orders from a Shopify store. 

## Client Issue

The client needed an automated solution to handle prescription files associated with orders from their Shopify store. Each order contains a link to the prescription file, which is uploaded using the LensAdvisor app. The process involves the following steps:

1. An email is received with the order details and a link to the prescription.
2. The prescription link sometimes requires a login to access the file.
3. The prescription file (PDF, PNG, JPG) needs to be downloaded.
4. The downloaded file should be labeled with the order number.
5. The labeled file needs to be sent to the supplier via email.

## Solution Provided

To address the client's needs, a Python script was created to automate the entire process. The solution includes the following components:

1. **Email Fetching**: Using the `imaplib` and `email` libraries to connect to the email server, search for relevant emails, and extract order information and prescription links.
2. **Prescription Link Extraction**: Using `BeautifulSoup` to parse the email content and extract the prescription link.
3. **File Downloading**: Accessing the LensAdvisor API to download the prescription file.
4. **Email Sending**: Using `smtplib` to send an email with the prescription file attached to the supplier.
5. **Flask Web Interface** (Optional): A simple Flask app to manually trigger the script and monitor the process.

## Technologies Used

- **Python**: Core scripting language.
- **IMAPLIB**: For fetching emails.
- **BeautifulSoup**: For parsing HTML content.
- **Requests**: For making HTTP requests to the LensAdvisor API.
- **SMTPLIB**: For sending emails.
- **Flask** (Optional): For creating a web interface to trigger the script manually.
- **AWS EC2**: For hosting the script and running it in a scheduled manner using cron jobs.

## Setup Instructions

### Prerequisites

- An AWS account and EC2 instance.
- A Gmail account with IMAP enabled (or any other email provider with IMAP support).
- Python 3.x installed on the server.
- PuTTY for SSH access to the server (if using Windows).

### Step-by-Step Guide

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Shopify-Prescription-Automation.git
   cd Shopify-Prescription-Automation


**2. Set Up a Virtual Environment**

python3 -m venv venv
source venv/bin/activate

**3. Install Dependencies**

pip install -r requirements.txt


**4. Configure the Script**
Update the configuration section in prescription_automation.py with your email credentials, LensAdvisor token, and other necessary details.

**5. Run the Script**

python prescription_automation.py

**6. Set Up Automated Execution**
Add a cron job to run the script at regular intervals (e.g., every 15 minutes):

crontab -e
Add the following line:

*/15 * * * * /path/to/your/venv/bin/python /path/to/your/script/prescription_automation.py

**Optional: Run the Flask App**

python app.py


Access the web interface at http://yourserver:5000/run-script.


                      
