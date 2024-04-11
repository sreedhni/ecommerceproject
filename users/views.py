from django.utils.encoding import force_str 
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import login,authenticate,logout
from users.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str


from django.contrib.auth.tokens import PasswordResetTokenGenerator
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'register_seller.html')
        try:
            if User.objects.get(username=email):
                messages.info(request, "email is taken")
                return render(request, 'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email, email, password)
        user.is_active = False
        user.is_customer = True
        user.save()
        messages.success(request, "Account created successfully! An OTP was sent to your Email")
        return redirect("otp:verify-email",email=user.email)
    return render(request, "register_seller.html")

def signupseller(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'register_seller.html')
        try:
            if User.objects.get(username=email):
                messages.info(request, "email is taken")
                return render(request, 'register_seller.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email, email, password)
        user.is_active = False
        user.is_seller = True
        user.save()

        messages.success(request, "Activate your account by clicking the link in your gmail ")
        return redirect("otp:verify-email",email=user.email)
    return render(request, "register_seller.html")



class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None
        
        if user is not None and generate_token.check_token(user, token):
            if user.is_customer:  
                user.is_active = True
                user.save()
                messages.info(request, "Account activated successfully")
                return redirect('/users/login')
            elif user.is_seller:  
                user.is_active = False
                user.save()
                messages.info(request, "Account activated only when the admin alllows you")
                return redirect('/users/login')
            elif request.user.is_superuser: 
                user.is_active = True
                user.save()
                messages.info(request, "Account activated successfully")
                return redirect('/users/login')
            else:
                messages.error(request, "Activation failed. Insufficient permissions.")
                return render(request, 'activatefail.html')
        else:
            messages.error(request, "Activation failed. Invalid token.")
            return render(request, 'activatefail.html')

def handlelogin(request):
    if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/users/login')
        
    return render(request, 'login.html')





def handlelogout(request):
    logout(request)
    messages.info(request,"log out success")
    return redirect('/users/login')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'request-reset-email.html')
    def post(self, request):
        email=request.POST['email']
        user=User.objects.filter(email=email)
        if user.exists():


            email_subject='[Reset Your Password]'

            message=render_to_string('reset-user-password.html', {

            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': PasswordResetTokenGenerator().make_token(user[0])
             })
            email_message=EmailMessage(email_subject, message, settings.EMAIL_HOST_USER,
                [email])
            email_message.send()

            messages.info(request, "WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD")

            return render(request, 'request-reset-email.html')
from django.utils.encoding import DjangoUnicodeDecodeError

class SetNewPasswordView(View):
    def get(self, request, uidb64,token):
        context = {'uidb64':uidb64,'token':token}
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token): 
                messages.warning (request, "Password Reset Link is Invalid") 
                return render (request, 'request-reset-email.html')
        except DjangoUnicodeDecodeError as identifier: pass

        return render(request, 'set-new-password.html', context)

    def post(self, request, uidb64, token):
        context={'uidb64': uidb64,
                'token': token
}
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")

            return render(request, 'register.html')
        try:

            user_id=force_str(urlsafe_base64_decode (uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password (password)

            user.save()

            messages.success (request, "Password Reset Success Please Login with NewPassword")
            return redirect('/users/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Something Went Wrong")
            return render(request, 'set-new-password.html',context)
        return render(request, 'set-new-password.html',context)
    


