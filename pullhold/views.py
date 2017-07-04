from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View

from .forms import UserForm
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'pullhold/index.html')

def user_logout(request):
    logout(request)
    return redirect('pullhold:index')


class UserSignIn(View):

    def get(self, request):
        return render(request, 'pullhold/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('pullhold:index')

        else:
            error = "Invalid Username or Password"
            return render(request, 'pullhold/login.html', {'error': error})

class UserFormView(View):
    form_class = UserForm
    template_name = 'pullhold/registration.html'

    # display a black user sign up form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data and store in db
    def post(self, request):
        form = self.form_class(request.POST) # passes user input into form validation

        if form.is_valid() and form.data['password'] == form.data['password_confirm']:
            user = form.save(commit = False)

            #Clean/Normalize the databases
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password) #processes and stores password with proper hash
            user.save()

            #returns User objects if credentials are correct
            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('pullhold:index')

        return render(request, self.template_name, {'form': form , 'error': "Passwords DO NOT match!"})
