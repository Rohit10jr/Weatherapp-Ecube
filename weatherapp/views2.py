from django.shortcuts import render, redirect
from .forms import RegisterForm, CityForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User 
from django.shortcuts import render, get_object_or_404, redirect
from .models import City

import matplotlib.pyplot as plt
from django.shortcuts import render
import pandas as pd
import os
from django.conf import settings

import os
from dotenv import load_dotenv
from pathlib import Path
import requests

import folium

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import matplotlib.pyplot as plt
import mplcursors
from datetime import datetime,timedelta


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
user_api = os.environ['current_weather_data']
                      

@login_required(login_url="/login")
def city_detail(request):
    if request.method == 'POST':
        form  = CityForm(request.POST)
        if form.is_valid():
            city_form = form.save(commit=False)
            city_form.user = request.user
            city_form.save()
            new_form  = CityForm(request.POST)

            cities = City.objects.filter(user=request.user).order_by('-id')[:5]
            weather_data = get_weather_data(cities)
            request.session['weather_data'] = weather_data


            return render(request, 'main/home.html', {'cities': cities, 'form':new_form, 'weather_data' : weather_data})

    form = CityForm()

    cities = City.objects.filter(user=request.user).order_by('-id')[:5]
    weather_data = get_weather_data(cities)
    request.session['weather_data'] = weather_data

    return render(request, 'main/home.html', {'cities': cities, 'form':form, 'weather_data' : weather_data})

def get_weather_data(cities):
    weather_data = []  

    for city in cities:
        # url = base_url.format(city, user_api)
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'        
        url = url.format(city, user_api)
        PARAMS = {'units':'metric'}
        # city_weather = requests.get(url).json()
        # city_weather = requests.get(url).json()
        city_weather = requests.get(url,params=PARAMS).json()
        # weather = 1
        # print(city_weather)

        if 'cod' in city_weather and city_weather['cod'] == '404':
            # City not found, handle this case
            weather = {
                'name' : city.name,  
                'lon': 'N/A',
                'lat': 'N/A',

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
                'name' : city.name,  
                'lon': city_weather['coord'].get('lon', 'N/A'),
                'lat': city_weather['coord'].get('lat', 'N/A'),

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
                'name' : 'None',
                'lon': 'N/A',
                'lat': 'N/A',

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
    return weather_data
