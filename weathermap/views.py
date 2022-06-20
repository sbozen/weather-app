import os
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
import requests
import json
from decouple import config

API_KEY = config('API_KEY')  # API key from OpenWeatherMap

temp_dict = {}
city_list = []


def index(request):

    with open("tr.json", encoding="utf8") as data:
        cities = json.load(data)
        for i in cities:
            city_list.append(i['name'])

    if request.method == 'POST':
        city = request.POST['city']

        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        # url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}}&lang=tr'
        response = requests.get(url)
        data = response.json()
        main = data['weather'][0]['main']

        description = data['weather'][0]['description']
        temp = data['main'].get('temp') - 273.15
        format_float = "{:.2f}".format(temp)
        temp_dict['description'] = description
        temp_dict['temp'] = format_float + " °C"

        return render(request, 'base.html', {'data': temp_dict, 'cities': city_list, 'selected_city': city, 'main': main})

        # https: // api.openweathermap.org/data/2.5/weather?q = {city name} & appid = {API key}

    else:
        return render(request, 'base.html', {'data': '', 'cities': city_list, 'selected_city': 'Results'})
