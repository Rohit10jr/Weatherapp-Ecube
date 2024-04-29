from django.shortcuts import render, redirect
from .forms import RegisterForm, CityForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User 
from django.shortcuts import render, get_object_or_404, redirect
from .models import City
# rohit 1234 rohitjr !@@#$%^1234

@login_required(login_url="/login")
def city_detail(request):
    cities = City.objects.filter(user=request.user)
    if request.method == 'POST':
        form  = CityForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return render(request, 'main/mainbase.html', {'cities': cities, 'form':form})
    else:
        form = CityForm()
    # posts ={"greet": "hello"}
    return render(request, 'main/mainbase.html', {'cities': cities, 'form':form})


# model cities crud

# def city_create(request):
#     if request.method == 'POST':
#         form  = CityForm(request.POST)
#         if form.is_valid():
#             todo = form.save(commit=False)
#             todo.user = request.user
#             todo.save()
#             return render()
#     else:
#         form = CityForm()
#     return render(request, '', {})


def city_update(request, pk):
    city = get_object_or_404(City, id=pk, user=request.user)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('detail')
    else:
        form = CityForm(instance=city)  # Pass the city instance to the form
    return render(request, 'main/update.html', {'form': form, 'city':city})  # 


def city_delete(request, pk):
    city = get_object_or_404(City, id=pk, user=request.user)
    if request.method == 'POST':
        city.delete()
    # return redirect('home')
    return redirect('detail')




# registration login logout

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/app')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form": form})

# logout view
def user_logout(request):
    logout(request)
    return redirect('/login')