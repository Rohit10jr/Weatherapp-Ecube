from django.shortcuts import render, redirect
from .forms import RegisterForm, CityForm, LandingForm
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
# rohit 1234 rohitjr !@@#$%^1234

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
user_api = os.environ['current_weather_data']
# base_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}"
# PARAMS = {'units':'metric'}

@login_required(login_url="/login")
def city_detail(request):
    if request.method == 'POST':
        form  = CityForm(request.POST)
        if form.is_valid():
            city_form = form.save(commit=False)
            city_form.user = request.user
            city_form.save()
            new_form  = CityForm(request.POST)

            # cities = City.objects.filter(user=request.user).order_by('-id')[:5]
            cities = City.objects.filter(user=request.user).order_by('-created_at')[:5]
            weather_data = get_weather_data(cities)
            request.session['weather_data'] = weather_data


            return render(request, 'main/home.html', {'cities': cities, 'form':new_form, 'weather_data' : weather_data})


    form = CityForm()

    # cities = City.objects.filter(user=request.user).order_by('-id')[:5]
    # city = City.objects.filter(user=request.user).order_by('-id')[:5]
    # cities = City.objects.filter(user=request.user).order_by('-created_at').values('name').distinct()[:5]
    cities = City.objects.filter(user=request.user).order_by('-created_at')[:5]
    weather_data = get_weather_data(cities)
    request.session['weather_data'] = weather_data
    return render(request, 'main/home.html', {'cities': cities, 'form':form, 'weather_data' : weather_data})

def get_weather_data(cities):
    weather_data = []  

    # print(cities)

    for city in cities:
        # url = base_url.format(city, user_api)
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'        
        url = url.format(city, user_api)
        PARAMS = {'units':'metric'}
        city_weather = requests.get(url,params=PARAMS).json()

        if 'cod' in city_weather and city_weather['cod'] == '404':
            # City not found
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
                # 'name' : city.name,  
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
        # print(weather_data)
        
    return weather_data

# update and plot for landing page

def city_update(request, pk):
    city = get_object_or_404(City, id=pk, user=request.user)
    if request.method == 'POST':
        form = LandingForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('detail')
        
    weather_data = request.session.get('weather_data', None)

    city_weather_data = None
    for data in weather_data:
        if data['name'] == city.name.lower():
            city_weather_data = data
            # print(city_weather_data)
            break
    city_lon = city_weather_data['lon']
    city_lat = city_weather_data['lat']
        
    # ---------open-meteo-config-----------
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # ---------getting start and end date---------- 
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    formatted_date = current_date.strftime("%Y-%m-%d")
    date_14_days_ago = current_date - timedelta(days=14)

    try:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": city_lat,
            "longitude": city_lon,
            "start_date": date_14_days_ago,
            "end_date": formatted_date,
            "hourly": ["temperature_2m", "relative_humidity_2m"]
        }
        responses = openmeteo.weather_api(url, params=params)

        response = responses[0]
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        # print(hourly_dataframe)

        # Styling parameters
        temperature_color = '#FF0000'   # Red
        humidity_color = '#4287f5'      # Blue
        background_color = '#f0f0f0'    # Light Gray
        grid_color = '#CCCCCC'          # Light Gray
        font_size = 14
        font_family = 'Arial'

        # Plotting hourly temperature and humidity
        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.plot(hourly_dataframe['date'], hourly_dataframe['temperature_2m'], color=temperature_color, label='Temperature (°C)', linewidth=2)
        ax1.set_xlabel('Date and Time', fontsize=font_size, fontfamily=font_family, color='black')
        ax1.set_ylabel('Temperature (°C)', fontsize=font_size, fontfamily=font_family, color=temperature_color)
        ax1.tick_params(axis='y', labelcolor=temperature_color)
        ax1.set_title('Hourly Temperature and Relative Humidity', fontsize=font_size, fontweight='bold', fontfamily=font_family, color='black')
        ax1.grid(True, color=grid_color)
        ax1.tick_params(axis='both', which='major', labelsize=font_size)
        ax1.set_facecolor(background_color)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.tick_params(axis='x', labelrotation=45, labelsize=10)
        # Adding tooltips for temperature
        mplcursors.cursor(ax1, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f"{sel.artist.get_label()}: {sel.target[1]:.2f} °C")
        )

        # Creating secondary y-axis for humidity
        ax2 = ax1.twinx()

        # Plotting hourly relative humidity
        ax2.plot(hourly_dataframe['date'], hourly_dataframe['relative_humidity_2m'], color=humidity_color, label='Relative Humidity (%)', linewidth=2)
        ax2.set_ylabel('Relative Humidity (%)', fontsize=font_size, fontfamily=font_family, color=humidity_color)
        ax2.tick_params(axis='y', labelcolor=humidity_color)

        # Adding tooltips for relative humidity
        mplcursors.cursor(ax2, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f"{sel.artist.get_label()}: {sel.target[1]:.2f} %")
        )

        # Rotate x-axis labels to avoid overlapping
        plt.tight_layout()
        plt.xticks(rotation=45, fontsize=10)

        plot_path = os.path.join(settings.MEDIA_ROOT, 'temp_plot.png')
        plt.savefig(plot_path)
        
    except Exception as e:
        # print(e)
        plot_path = os.path.join(settings.MEDIA_ROOT, '')
    form = LandingForm(instance=city) 
    return render(request, 'main/loading.html', {'form': form, 'city':city, 'weather_data':weather_data, 'plot_path': plot_path})  


#  delete cities
def city_delete(request, pk):
    city = get_object_or_404(City, id=pk, user=request.user)
    if request.method == 'POST':
        city.delete()
    # return redirect('home')
    return redirect('detail')

# registration 
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

# logout page
def user_logout(request):
    logout(request)
    return redirect('/login')

# about page
def about(request):
    return render(request, 'main/about.html')