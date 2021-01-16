from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.contrib.auth.models import User





GENDER_CHOICES = (('E', 'Erkek'), ('K', 'Kadın'), ('B', 'Belirtmek İstemiyorum'))

# class MyForm(forms.Form):
#     i_agree = forms.BooleanField()

class LoginForm(forms.Form):

    username = forms.CharField(label = "Kullanıcı Adı")
    password = forms.CharField(label = "Parola" ,widget = forms.PasswordInput)

class RegisterForm(forms.Form):

    username = forms.CharField(max_length= 50, label = "Kullanıcı Adı")
    password = forms.CharField(max_length= 20, label = "Parola",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length= 20, label = "Parola Dogrula", widget = forms.PasswordInput)
    email = forms.EmailField(max_length = 254,label="Email")
    birth_date = forms.DateField(help_text='Bu Şekilde Olur: GG-AA-YY',label = "Doğum Tarihi")

    # i_agree = forms.BooleanField()
    gender = ChoiceField(widget=RadioSelect, choices=GENDER_CHOICES,label="Cinsiyet")
    

    class Meta:
        model = User

        fields = ('username','password','confirm','email',"gender","birth_date")    
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        email = self.cleaned_data.get("email")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor.")
        # if User.objects.get(username) in username:
        #     raise forms.ValidationError("Bu Kullanıcı Adı Kullanılmaktadır.")
        values = {
            "username": username,
            "password": password,
            "email": email,

        }
        return values
        