import json
import urllib
from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def register(request):
    
    
    form = RegisterForm(request.POST or None)

    if form.is_valid():

        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
            

        if result['success']:
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            

            Buraya = 'http://localhost:8000/user/confirm'
            template = render_to_string("mail_body.html",{'name':username,'Buraya':Buraya})
            sendmail = EmailMessage(

                'Kayıdını Tamamla ! ',
                template,
                settings.EMAIL_HOST_USER,
                [email],

            )
            sendmail.content_subtype = "html"
            sendmail.fail_silenty=False
            sendmail.send()


            # username = form.cleaned_data.get("username")
            # password = form.cleaned_data.get("password")
            # email = form.cleaned_data.get("email")
            

            newUser = User(username = username)
            newUser.set_password(password)
            newUser.email = email

            

            newUser.save()
            # login(request,newUser)
            # messages.success(request, "Başarıyla Kayıt Oldunuz. Lütfen Hesabınızı E-Mailinize Gelen Link İle Doğrulayınız..")
            return render(request,"success.html")
        
        else:
            messages.info(request,  "reCAPTCHA'yı Lütfen Doğrulayınız.")
            context = {
            "form":form
            }
            return render(request,"register.html",context)

            

        

    context = {
            "form":form
         }
    return render(request,"register.html",context)








    # if request.method == "POST":
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password")

    #         newUser = User(username = username)
    #         newUser.set_password(password)
    #         newUser.save()
    #         login(request,newUser)
    #         return redirect("index")
    #     context = {
    #         "form":form
    #     }
    #     return render(request,"register.html",context)
        

    # else:
    #     form = RegisterForm()
    #     context = {
    #         "form":form
    #     }
    #     return render(request,"register.html",context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        form = LoginForm(request.POST or None)
        context = {
            "form" : form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username") 
            password = form.cleaned_data.get("password")
            user = authenticate(username = username,password = password)
            if user is None:
                messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
                return render(request,"login.html",context)
            messages.success(request,"Başarıyla giriş yapıldı")
            login(request,user)
            return redirect("index")
        return render(request,"login.html",context)
def logoutUser(request):

    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("index")

def Terms(request):
    

    return render(request,"terms.html")

def confirm(request):
    

    return render(request,"confirm_template.html")
def success(request):

    return render(request,"success.html")