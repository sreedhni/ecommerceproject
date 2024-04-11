from django.db import models
import secrets

from users.models import User
class OtpToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username
    