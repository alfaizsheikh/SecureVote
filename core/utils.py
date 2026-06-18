import random
import string
from django.utils import timezone
from .models import OTPVerification

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_sms(mobile_number, otp):
    """
    Send OTP via SMS. For testing purposes, we'll just print to console.
    In production, integrate with SMS service like Twilio, AWS SNS, etc.
    """
    print(f"SMS to {mobile_number}: Your SecureVote OTP is {otp}. Valid for 10 minutes.")
    # In production, replace with actual SMS sending logic
    return True

def create_and_send_otp(mobile_number):
    """Create OTP record and send SMS"""
    # Delete any existing OTP for this mobile number
    OTPVerification.objects.filter(mobile_number=mobile_number, is_verified=False).delete()
    
    # Generate new OTP
    otp = generate_otp()
    
    print(f"Generated OTP: {otp}")
    # Create OTP record
    otp_record = OTPVerification.objects.create(
        mobile_number=mobile_number,
        otp_code=otp
    )
    
    # Send SMS
    if send_otp_sms(mobile_number, otp):
        return otp
    else:
        otp_record.delete()
        return None

def verify_otp(mobile_number, otp_code):
    """Verify OTP code"""
    try:
        otp_record = OTPVerification.objects.get(
            mobile_number=mobile_number,
            otp_code=otp_code,
            is_verified=False
        )
        
        if otp_record.is_expired():
            return False, "OTP has expired. Please request a new one."
        
        # Mark as verified
        otp_record.is_verified = True
        otp_record.save()
        
        return True, "OTP verified successfully!"
        
    except OTPVerification.DoesNotExist:
        return False, "Invalid OTP. Please check and try again."

