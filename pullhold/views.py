from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import ComicTitle, Publisher, UserProfile
from .forms import UserForm, ComicTitleForm
from .comicvine import comicvine

# Create your views here.
class IndexView(View):
    def get(self, request):
        form = UserForm
        return render(request, 'pullhold/index.html', {'form': form})


class PullHoldMenuView(View):
    def get(self, request):
        if request.user.is_authenticated:
            first_name = request.user.first_name
            last_name = request.user.last_name
            greeting = "Welcome {0} {1}!" .format(first_name, last_name)
            return render(request, 'pullhold/pullhold.html', {'greeting': greeting})
        else:
            return redirect('pullhold:login')


class PullHoldAddView(View):
    def get(self, request):

        if request.user.is_authenticated:
            #filter is currently filtering publishers by publisher.id
            current_available_comics = ComicTitle.objects.all()
            marvel = []
            dc_comics = []
            other = []

            for i in current_available_comics:
                if(i.publisher.publisher_name == 'Marvel'):
                    marvel.append(i)
                elif(i.publisher.publisher_name == 'DC Comics'):
                    dc_comics.append(i)
                else:
                    other.append(i)

            return render(request, 'pullhold/pulladd.html', {'marvel': marvel,
            'other':other, 'dc_comics': dc_comics})

        else:
            return redirect('pullhold:login')

    def post(self, request):
        user = request.user
        add_list = request.POST.getlist('comic')

        #check to see if comic is in users holdlist, if not add it
        for i in add_list:
            if not user.userprofile.comics.filter(id = i).exists():
                user.userprofile.comics.add(i)
                comic = ComicTitle.objects.get(id = i)
                comic.reservations +=1
                comic.save()
            user.save()

        holdlist = user.userprofile.comics.all().order_by('comic_title')
        return redirect('pullhold:holdlist')


class HoldListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            holdlist = user.userprofile.comics.all().order_by('comic_title')
            return render(request, 'pullhold/holdlist.html', {'holdlist': holdlist})

        else:
            return redirect('pullhold:login')

    def post(self, request):
        user = request.user
        remove_list = request.POST.getlist('remove')

        #remove comic is in users holdlist
        for i in remove_list:
            user.userprofile.comics.remove(i)
            comic = ComicTitle.objects.get(id = i)
            comic.reservations -= 1
            comic.save()
        user.save()

        holdlist = user.userprofile.comics.all().order_by('comic_title')
        return render(request, 'pullhold/holdlist.html', {'holdlist': holdlist})


def user_logout(request):
    logout(request)
    request.session['logged_out'] = True
    return redirect('home')


class ComicTitleSearchView(View):

    def get(self, request):
        return render(request, 'pullhold/newcomicsearch.html', )

    def post(self, request):
        search_term = request.POST['comic_title']
        api_results = comicvine(search_term)

        results = []
        for i in api_results:
            individual_title = [i['name']]
            individual_title.append(i['image']['small_url'])
            individual_title.append(i['publisher'])
            individual_title.append(i['start_year'])
            results.append(individual_title)

        return render(request, 'pullhold/newcomicresults.html', {'results': results})


class AddNewComicTitleView(View):

    def get(self, request):
        return render(request, 'pullhold/newcomicsearch.html', )

    def post(self, request):
        new_title = request.POST['comic_title']
        current_titles = ComicTitle.objects.values_list('comic_title', flat = True)
        new_title_publisher = request.POST['publisher']
        current_publishers = Publisher.objects.values_list('publisher_name', flat = True)


        if(new_title not in current_titles):

            if(new_title_publisher not in current_publishers):
                new_publisher = Publisher()
                new_publisher.publisher_name = new_title_publisher
                new_publisher.save()

            new_comic = ComicTitle()
            new_comic.comic_title = request.POST['comic_title']
            new_comic.cover_art = request.POST['cover_art']
            new_comic.publisher = Publisher.objects.get(publisher_name = request.POST['publisher'])
            new_comic.save()

        return redirect('pullhold:pulladd')


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
