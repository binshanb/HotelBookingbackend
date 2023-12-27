# helper.py
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()

# Initialize Twilio client
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
service = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])

# Function to send OTP to a phone number
def send_otp(phone):
    default_country_code = "+91"

    if phone.startswith("+"):
        formatted_phone = phone
    else:
        formatted_phone = default_country_code + phone

    try:
        service.verifications.create(to=formatted_phone, channel='sms')
        return True
    except TwilioRestException as e:
        print(f"Failed to send OTP: {e}")
        return False

# Function to verify OTP code for a phone number
def verify_otp(phone,code):
    try:
        result = service.verification_checks.create(to=phone,code=code)
        return result.status == 'approved'
    except TwilioRestException as e:
        print(f"TwilioRestException: {e}")
        return False
















