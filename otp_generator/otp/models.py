from django.db import models
# from merchant.models import Merchant


# Create your models here.
class OTP(models.Model):
    # merchant_id = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20)
    otp_generated = models.CharField(max_length=6, null=True)
