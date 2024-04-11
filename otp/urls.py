from django.urls import path
from . import views 

app_name="otp"
urlpatterns = [

path('verify-email/<str:email>/', views.verify_email, name='verify-email'),
    path("resend-otp", views.resend_otp, name="resend-otp"),
]
