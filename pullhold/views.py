from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import ComicTitle, Publisher
from .forms import UserForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        greeting = "Welcome {0}!" .format(username)
    elif request.session.get('logged_out') == True:
        greeting = "You are successfully logged out."
    else:
        greeting = ""
    return render(request, 'pullhold/index.html', {'greeting': greeting})


class PullHoldView(View):
    def get(self, request):
        marvel = 1
        image = 2
        dc = 3

        publishers = Publisher.objects.all()
        marvel = ComicTitle.objects.filter(publisher = 1)
        image = ComicTitle.objects.filter(publisher = 2)
        dc_comics = ComicTitle.objects.filter(publisher = 3)

        return render(request, 'pullhold/pullhold.html', {'publishers': publishers,
        'marvel': marvel, 'image':image, 'dc_comics': dc_comics})

    def post(self, request):
        pass

def user_logout(request):
    logout(request)
    request.session['logged_out'] = True
    return redirect('home')


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
