'''
from allauth.account.adapter import DefaultAccountAdapter
from .models import UserProfile

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
          # Save the user object to the database first
        user_profile = UserProfile(user=user)
        #user_profile.save()
        user.save()
        
        return user

'''