from django.shortcuts import render, redirect
from .forms import RegisterForm, CityForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User 
from django.shortcuts import render, get_object_or_404, redirect
from .models import City

import os
from dotenv import load_dotenv
from pathlib import Path
import requests
# rohit 1234 rohitjr !@@#$%^1234

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
user_api = os.environ['current_weather_data']
# base_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}"
# PARAMS = {'units':'metric'}

@login_required(login_url="/login")
def city_detail(request):
    cities = City.objects.filter(user=request.user)
    weather_data = []  

    for city in cities:
        # url = base_url.format(city, user_api)
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'        
        url = url.format(city, user_api)
        PARAMS = {'units':'metric'}
        # city_weather = requests.get(url).json()
        # city_weather = requests.get(url).json()
        city_weather = requests.get(url,params=PARAMS).json()
        weather = 1
        print(city_weather)

        if 'cod' in city_weather and city_weather['cod'] == '404':
            # City not found, handle this case
            weather = {
                'city' : city.name,  
                'temperature' : 'N/A',
                'humidity' : 'N/A',
                'pressure' : 'N/A',
                'sea_level' : 'N/A',
                'clouds': 'N/A', 
                'temp_max' : 'N/A',
                'temp_min' : 'N/A',
                'wind_speed' : 'N/A',
                'wind_deg' : 'N/A',
                'country' : 'N/A',
                'description' : 'City not found',
                'icon' : 'N/A',
            }

        elif 'weather' in city_weather and 'main' in city_weather:
            weather = {
                'city' : city.name,  
                'temperature' : city_weather['main'].get('temp', 'N/A'),
                'humidity' : city_weather['main'].get('humidity', 'N/A'),
                'pressure' : city_weather['main'].get('pressure', 'N/A'),
                'sea_level' : city_weather['main'].get('sea_level', 'N/A'),

                'clouds': city_weather['clouds'].get('all', 'N/A'),
                'temp_max' : city_weather['main'].get('temp_max', 'N/A'),
                'temp_min' : city_weather['main'].get('temp_min', 'N/A'),
                'wind_speed' : city_weather['wind'].get('speed', 'N/A'),
                'wind_deg' : city_weather['wind'].get('deg', 'N/A'),

                'country' : city_weather['sys'].get('country', 'N/A'),
                'description' : city_weather['weather'][0].get('description', 'City not found',),
                'icon' : city_weather['weather'][0].get('icon', 'N/A'),
            }
        else:
            weather = {
                'city' : 'None',
                'temperature' : 'N/A',
                'humidity' : 'N/A',
                'pressure' : 'N/A',
                'sea_level' : 'N/A',
                'clouds': 'N/A', 
                'temp_max' : 'N/A',
                'temp_min' : 'N/A',
                'wind_speed' : 'N/A',
                'wind_deg' : 'N/A',
                'country' : 'N/A',
                'description' : 'City not found',
                'icon' : 'N/A'
            }
        weather_data.append(weather)

        # if 'weather' in city_weather and 'main' in city_weather:
        #     weather = {
        #         'city' : city,
        #         'description' : city_weather['weather'][0]['description'],
        #         'temperature' : city_weather['main']['temp'],
        #         'icon' : city_weather['weather'][0]['icon']
        #     }
        #     # weather_data.append(weather)
        # else:
        #     weather = {
        #         'city' : 'none',
        #         'description' : 'none',
        #         'temperature' : 'none',
        #         'icon' : 'none'
        #     }
        # weather_data.append(weather)

    # weather_data = {
    #     'city' : 'none',
    #     'description' : 'none',
    #     'temperature' : 'none',
    #     'icon' : 'none'
    # }
    
    # Store weather_data list in session
    # print('----------detail - weather_data-----------')
    # print(weather_data)
    # request.session['city_weather'] = weather_data
    # city_weather_api = request.session['city_weather']
    # print('----------detail-----------')
    # print(city_weather_api)
    # print('-----------------------')
    if request.method == 'POST':
        form  = CityForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return render(request, 'main/mainbase.html', {'cities': cities, 'form':form, 'weather_data' : weather_data})
    else:
        form = CityForm()
    # posts ={"greet": "hello"}
    return render(request, 'main/mainbase.html', {'cities': cities, 'form':form, 'weather_data' : weather_data})


def city_update(request, pk):
    weather_data = request.session.get('city_weather', None)
    
    print("--------update--------")
    print(weather_data)
    print("----------------")

    city = get_object_or_404(City, id=pk, user=request.user)
    print(city)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('detail')
    else:
        form = CityForm(instance=city)  # Pass the city instance to the form
    return render(request, 'main/update.html', {'form': form, 'city':city, 'weather_data':weather_data})  # 


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