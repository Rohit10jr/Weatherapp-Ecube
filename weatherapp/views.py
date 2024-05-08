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
# rohit 1234 rohitjr !@@#$%^1234

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
user_api = os.environ['current_weather_data']
# base_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}"
# PARAMS = {'units':'metric'}

@login_required(login_url="/login")
def city_detail(request):
    cities = City.objects.filter(user=request.user).order_by('-id')[:5]
    # cities = City.objects.filter(user=request.user).order_by('-created_at').values('name').distinct()[:5]
    # cities = City.objects.filter(user=request.user).order_by('-id').values('name').distinct()[:5]
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
            return render(request, 'main/dark.html', {'cities': cities, 'form':form, 'weather_data' : weather_data})
    else:
        form = CityForm()
    # posts ={"greet": "hello"}
    request.session['weather_data'] = weather_data
    return render(request, 'main/dark.html', {'cities': cities, 'form':form, 'weather_data' : weather_data})


def city_update(request, pk):
    # weather_data = request.session.get('city_weather', None)
    weather_data = request.session.get('weather_data', None)

    print("-------update-------")
    print(weather_data)
    print("--------------------")

    city = get_object_or_404(City, id=pk, user=request.user)
    print("--------city--------")
    print(city)
    print("--------------------")

    city_weather_data = None
    for data in weather_data:
        if data['name'] == city.name:
            city_weather_data = data
            break
    city_lon = city_weather_data['lon']
    city_lat = city_weather_data['lat']

    print("-----lat and lon-----")
    print(f'city_lat={city_lat} and city_lon={city_lon}')
    print("----------------------")

    # ---------open-meteo-config-----------
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # ---------getting start and end date---------- 
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    formatted_date = current_date.strftime("%Y-%m-%d")
    date_14_days_ago = current_date - timedelta(days=14)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": city_lat,
        "longitude": city_lon,
        "start_date": date_14_days_ago,
        "end_date": formatted_date,
        "hourly": ["temperature_2m", "relative_humidity_2m"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
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

    # Plot temperature
    plt.plot(hourly_dataframe['date'], hourly_dataframe['temperature_2m'], label='Temperature (°C)', color='red')

    # Plot relative humidity
    plt.plot(hourly_dataframe['date'], hourly_dataframe['relative_humidity_2m'], label='Relative Humidity (%)', color='blue')

    # Adding labels and title
    plt.xlabel('Date and Time')
    plt.ylabel('Value')
    plt.title('Hourly Temperature and Relative Humidity')
    plt.legend()
    plt.grid(True)

    plot_path = os.path.join(settings.MEDIA_ROOT, 'temp_plot.png')
    # plt.savefig(plot_path)

    # Save the plot to a temporary file
    # plot_path = os.path.join(settings.STATIC_ROOT, 'temp_plot.png')
    plt.savefig(plot_path)

    # Show plot
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('detail')
    else:
        form = CityForm(instance=city)  # Pass the city instance to the form
    return render(request, 'main/update.html', {'form': form, 'city':city, 'weather_data':weather_data, 'plot_path': plot_path})  # 


def city_delete(request, pk):
    city = get_object_or_404(City, id=pk, user=request.user)
    if request.method == 'POST':
        city.delete()
    # return redirect('home')
    return redirect('detail')

# -------------ploting graphs-------------

def plot2(request):
    url="https://archive-api.open-meteo.com/v1/archive?latitude=13.0878&longitude=80.2785&start_date=2024-04-15&end_date=2024-04-29&hourly=temperature_2m,relative_humidity_2m"
    openmeteo_plot = requests.get(url).json()
    return render(request, 'main/plot2.html', {'openmeteo_plot': openmeteo_plot})

def plot_graph(request):
    # Sample data (replace with your actual data)
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
    temperature = [20, 22, 23, 25, 24, 22, 21]
    humidity = [50, 55, 60, 65, 70, 75, 80]

    # Create a dataframe from the data
    data = {'Day': days, 'Temperature': temperature, 'Humidity': humidity}
    df = pd.DataFrame(data)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(df['Day'], df['Temperature'], marker='o', label='Temperature (°C)')
    plt.plot(df['Day'], df['Humidity'], marker='o', label='Humidity (%)')
    plt.title('Temperature and Humidity Variation Over 7 Days')
    plt.xlabel('Day')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Save the plot to a temporary file
    # plot_path = 'weatherapp/static/temp_plot.png'
    # plot_path = os.path.join(settings.STATIC_URL, 'temp_plot.png')
    # plt.savefig(plot_path)

    plot_path = os.path.join(settings.MEDIA_ROOT, 'temp_plot.png')
    # plt.savefig(plot_path)

    # Save the plot to a temporary file
    # plot_path = os.path.join(settings.STATIC_ROOT, 'temp_plot.png')
    plt.savefig(plot_path)

    # Pass the plot path to the template
    return render(request, 'main/plot.html', {'plot_path': plot_path})


''' map view '''

def map(request):
    # mymap = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

    # Add a marker to the map
    # folium.Marker(
    #     location=[37.7749, -122.4194],
    #     popup="San Francisco",
    #     icon=folium.Icon(color="blue")
    # ).add_to(mymap)
    cities=[]
    city1 = {
        'lat': '37.7749',
        'lon': '-122.4194',
        'popup': 'san franscisco',
    }
    cities.append(city1)
    city2 = {
        'lat': '19.0760',
        'lon': '72.8777',
        'popup': 'mumbai',
    }
    cities.append(city2)
    city3 = {
        'lat': '39.9042',
        'lon': '116.4074',
        'popup': 'beijing',
    }
    cities.append(city3)
    # return render(request, 'main/mainbase.html', {'cities': cities, 'form':form, 'weather_data' : weather_data})
    return render(request, 'main/maptry.html', {'cities': cities})

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