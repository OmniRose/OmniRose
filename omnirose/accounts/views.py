from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login

from .forms import RegistrationForm
from .models import User

class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User

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


        # FIXME - send password in email here and tell user that on screen.
        print user.email, password

        return redirect('home')
