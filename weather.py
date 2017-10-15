import geocoder
import forecastio
import datetime

from menu import weather_menu

def get_location(loc):
    geo = geocoder.google(loc)  # get location based on user's argument string using google api
    latitude = geo.latlng[0]
    longtitude = geo.latlng[1]

    # get country and city
    return geo.json['address'], latitude, longtitude

def get_current_weather(loc, time):

    location, latitude, longtitude = get_location(loc)

    # get weather via OpenWeatherMap
    api_key = '74cc62440986d98d97347fef6bb55077'
    forecast = forecastio.load_forecast(api_key, latitude, longtitude, units='auto')  # request to OWM API
    
    reply_markup = None
    additional_response = ''

    # get required time based on user string
    if (time == None) or (time == 'now'):
        forecastData = forecast.currently()
        summary = forecastData.summary
        icon = forecastData.icon
        temperature = forecastData.temperature
        wind_speed = forecastData.windSpeed
        response = ''.join([str(summary), '\nTemp: ', str(temperature), '\nWind speed: ', str(wind_speed)])
    elif (time == 'minutely'):
        forecastData = forecast.minutely()
        summary = forecastData.summary
        icon = forecastData.icon
        temperature = forecast.currently().temperature
        response = ''.join([str(summary), '\nTemp: ', str(temperature)]) 
    elif (time == 'hourly'):
        forecastData = forecast.hourly()
        summary = forecastData.summary
        icon = forecastData.icon
        data = forecastData.data
        response = summary
        reply_markup = weather_menu(loc, time)
    elif (time == 'daily'):
        forecastData = forecast.daily()
        summary = forecastData.summary
        icon = forecastData.icon
        data = forecastData.data
        response = summary
        reply_markup = weather_menu(loc, time)
    return response, str(icon), location, reply_markup

def get_additional_info(loc, time):
    print('start')
    location, latitude, longtitude = get_location(loc)

    # get weather via OpenWeatherMap

    api_key = '74cc62440986d98d97347fef6bb55077'
    forecast = forecastio.load_forecast(api_key, latitude, longtitude, units='auto')  # request to OWM API

    additional_response = ''
    if time == 'hourly':
        data = forecast.hourly().data
        for hourly_data in data:
            time = hourly_data.time
            summary = hourly_data.summary
            temperature = hourly_data.temperature
            new_response = ''.join([additional_response, str(time), ' ', str(summary), ' Temp: ', str(temperature), '\n'])
            additional_response = new_response
    if time == 'daily':
        data = forecast.daily().data
        for daily_data in data: 
            time = daily_data.time
            summary = daily_data.summary
            temperature_high = daily_data.apparentTemperatureHigh
            temperature_low = daily_data.apparentTemperatureLow
            new_response = ''.join([additional_response, str(time), ' ', str(summary), ' Temp: ', str(temperature_low), '-', str(temperature_high), '\n'])
            additional_response = new_response

    print('finish')
    return additional_response