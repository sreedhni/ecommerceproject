from django.urls import path
from users import views
appname="users"
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.handlelogin,name="handlelogin"),
    path('signupseller/',views.signupseller,name="signupseller"),

    path('logout/',views.handlelogout,name="handlelogout"),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name="request-reset-email"),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name="set-new-password"),



   
]
