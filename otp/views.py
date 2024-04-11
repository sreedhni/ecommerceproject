from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import OtpToken
from django.contrib import messages
from users.models import User
from django.utils import timezone
from django.core.mail import send_mail


def verify_email(request, email):
    user = User.objects.get(username=email)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    if request.method == 'POST':
        if user_otp.otp_code == request.POST['otp_code']:
            if user_otp.otp_expires_at > timezone.now():
                if user.is_customer:
                    user.is_active = True
                    user.save()
                    messages.success(request, "Account activated successfully!! You can Login.")
                    return redirect("/users/login")
                elif user.is_seller:
                    user.is_active = False
                    user.save()
                    messages.info(request, "Account activated only when the admin allows you")
                    return redirect("/users/login")
                elif request.user.is_superuser: 
                    user.is_active = True
                    user.save()
                    messages.success(request, "Account activated successfully")
                    return redirect('/users/login')
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("otp:verify-email", email=user.email)
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("otp:verify-email", email=user.email)
        
    context = {}
    return render(request, "verify_token.html", context)



def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.email}
                                
                                """
            sender = "ecommerse@gmail.com"
            receiver = [user.email, ]
        
        
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", email=user.email)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "resend_otp.html", context)




