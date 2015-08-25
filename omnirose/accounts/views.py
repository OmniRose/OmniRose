from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.conf import settings

from template_email import TemplateEmail

from .forms import RegistrationForm
from .models import User

class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get('next')
        next_url = self.request.POST.get('next', next_url)
        if next_url:
            context['next'] = next_url
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        password = User.objects.make_random_password()
        obj.set_password(password)

        obj.is_active = True
        obj.save()

        # Now log in this user
        user = authenticate(email=obj.email, password=password)
        if user is not None:
            login(self.request, user)
        else:
            raise Exception("Could not auth recently created user")

        # send password in email
        email = TemplateEmail(
            to=[user.email],
            template='accounts/new_user_email.txt',
            context={ 'user': user, 'password': password, 'BASE_URL': settings.BASE_URL }
        )
        email.send()

        # where to next? If we have a next go there, otherwise home
        next_url = self.request.POST.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('home')


class EnterView(TemplateView):
    template_name = 'accounts/enter.html'

    def get_context_data(self, **kwargs):
        context = super(EnterView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', None)
        return context
