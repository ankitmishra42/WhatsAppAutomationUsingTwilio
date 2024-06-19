import csv
import logging
import os
from time import sleep
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_PHONE_NUMBER')

print(account_sid)
print(auth_token)
print(twilio_whatsapp_number)

# Check if environment variables are loaded
if not all([account_sid, auth_token, twilio_whatsapp_number]):
    logging.error("One or more Twilio environment variables are missing.")
    exit(1)

# Create a Twilio client
client = Client(account_sid, auth_token)

# Message content
message_body = "Hello, this is a test message from Ankit Mishra!"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send WhatsApp message with retry mechanism
def send_whatsapp(to_phone_number, from_phone_number, message, retries=3):
    for attempt in range(retries):
        try:
            message = client.messages.create(
                to=f'whatsapp:{to_phone_number}',
                from_=f'whatsapp:{from_phone_number}',
                body=message
            )
            logging.info(f"WhatsApp message sent to {to_phone_number}: {message.sid}")
            return True
        except Exception as e:
            logging.error(f"Failed to send WhatsApp message to {to_phone_number} on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying to send WhatsApp message to {to_phone_number} (attempt {attempt + 2}/{retries})...")
                sleep(1)  # Wait before retrying
    return False

# Function to read phone numbers from CSV file and send WhatsApp messages
def send_mass_whatsapp(file_path, rate_limit_per_sec=1):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                phone_number = row['phone_number']
                send_whatsapp(phone_number, twilio_whatsapp_number, message_body)
                sleep(1 / rate_limit_per_sec)  # Rate limiting to 1 message per second
    except FileNotFoundError:
        logging.error(f"CSV file not found: {file_path}")
    except Exception as e:
        logging.error(f"An error occurred while reading the CSV file: {e}")

# Path to the CSV file
csv_file_path = 'C:/Users/lenovo/Desktop/whatssp1/phone_numbers.csv'

# Start the script
logging.info("Starting the WhatsApp message sending script.")

# Sending up to 3600 messages per hour
send_mass_whatsapp(csv_file_path)

# End the script
logging.info("Finished sending WhatsApp messages.")
