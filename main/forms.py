from dataclasses import field
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ProductReview, UserAddressBook

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email','username','password1','password2')


class ProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email','username')


#Review form
class ReviewForm(forms.ModelForm):
    class Meta:
        model=ProductReview
        fields=('review_text','review_rating')


class AddressBookForm(forms.ModelForm):
    class Meta:
        model=UserAddressBook
        fields=('address','mobile','status')




