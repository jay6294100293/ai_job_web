from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
class CustomLoginView(LoginView):
    template_name = './auth_app/login.html'

    def get_success_url(self):

        messages.success(self.request, 'Successfully logged in!')
        return reverse('dashboard')  # Redirect to dashboard after successful login
