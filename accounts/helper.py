

from twilio.rest import Client
import os

# Load Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_SID = os.environ.get('TWILIO_VERIFY_SERVICE_SID')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
service = client.verify.services(TWILIO_VERIFY_SERVICE_SID)

# Function to send OTP via Twilio
def send_otp(phone_number):
    try:
        verification = service.verifications.create(to=phone_number, channel='sms')
        print(verification,"verify")
        return verification.sid
    except Exception as e:
        return None

# Function to verify OTP using Twilio
def verify_otp(phone_number, code):
    try:
        verification_check = service.verification_checks.create(to=phone_number, code=code)
        return verification_check.status == 'approved'
    except Exception as e:
        return False
















