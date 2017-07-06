from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import ComicTitle, Publisher
from .forms import UserForm

# Create your views here.
def index(request):
        return render(request, 'pullhold/index.html')


class PullHoldView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            greeting = "Welcome {0}!" .format(username)
            return render(request, 'pullhold/pullhold.html', {'greeting': greeting})
        else:
            return redirect('pullhold:login')


class PullHoldAddView(View):
    def get(self, request):

        if request.user.is_authenticated:
            #filter is currently filtering publishers by publisher.id
            publishers = Publisher.objects.all()
            marvel = ComicTitle.objects.filter(publisher__publisher_name="Marvel")
            image = ComicTitle.objects.filter(publisher__publisher_name="Image")
            dc_comics = ComicTitle.objects.filter(publisher__publisher_name="DC Comics")

            return render(request, 'pullhold/pulladd.html', {'publishers': publishers,
            'marvel': marvel, 'image':image, 'dc_comics': dc_comics})

        else:
            return redirect('pullhold:login')

    def post(self, rquest):
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
