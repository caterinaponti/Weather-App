#Caterina Ponti
#CS 110 Final Project 
#Weather Insights: A Visual Exploration of Weather Patterns

from flask import Flask, render_template_string, render_template, url_for, redirect
from flask import request
#Import OWM to get weather data from API 
from pyowm import OWM
#Import datetime to dispaly in the web app the time and date for San Francisco 
from datetime import datetime, timedelta
#to format API response 
from pyowm.utils import timestamps, formatting

#Import csv to get latitude and longitude of U.S. capitals map
import csv
#Import folium to display the US capitals maps
import folium

#Import Geopy to get the coords of a location (for the get_air_pollution function)
from geopy.geocoders import Nominatim 

#Import matplotlib.pyplot to display the forecast weather map 
import matplotlib.pyplot as plt

#File path operations with hourly_forecast.png
import os

app = Flask(__name__, template_folder='Templates', static_url_path='/static')
app.debug = True

owm = OWM('0e884fdc78cdf0265beca2ced044fbeb')
mgr = owm.weather_manager()

time_difference_hours = -8 #define difference hours 
now = datetime.utcnow() #Get the current date and time in UTC (Universal Time)
# Calculate the time in Los Angeles
now_sf = now + timedelta(hours=time_difference_hours)

# Format the Los Angeles time as a string
dt_string_sf = now_sf.strftime("%d/%m/%Y %H:%M:%S")

def getCurrentWeather(city, country):
	#Get current weather observation for specified city and country
	observation = mgr.weather_at_place(city + ',' + country)
	weather = observation.weather
	short_status = weather.status              #Extract short version of status (eg. 'Rain')
	detailed_status = weather.detailed_status  #Extract detailed version of status (eg. 'light rain')
	
	return detailed_status 

def getWeather(city, country):
	location = city +','+ country  #Combine the city and country into a location string
	observation = mgr.weather_at_place(location)
	w = observation.weather  
	fahrenheit_temperature = w.temperature('fahrenheit') #Get the temperature in Fahrenheit and Celsius
	celsius_temperature = w.temperature('celsius')

	return fahrenheit_temperature, celsius_temperature

#This function gets the wind speed in meters per second 
def getWind(city, country):
	observation = mgr.weather_at_place(city + ',' + country)  # 'weather_at_place'  method to obtain the weather observation
	wind_dict_in_meters_per_sec = observation.weather.wind()   # Default unit: 'meters_sec'
	
	return wind_dict_in_meters_per_sec

#This function gets barometric pressure information 
def getPressure(city, country):
	observation = mgr.weather_at_place(city + ',' + country)
	pressure_dict = observation.weather.barometric_pressure()
	
	return pressure_dict

#This function gets rain information 
def getRain(city, country):
	observation = mgr.weather_at_place(city + ',' + country)
	rain_dict = observation.weather.rain
	
	return rain_dict

#This function gets sunrise time in Unix timestamps, ISO format, and date format 
def getSunrise(city, country):
	observation = mgr.weather_at_place(city + ',' + country)
	weather = observation.weather
	sunrise_unix = weather.sunrise_time() # default unit: 'unix'
	sunrise_iso = weather.sunrise_time(timeformat='iso')
	sunrise_date = weather.sunrise_time(timeformat='date')
	
	return sunrise_unix, sunrise_iso, sunrise_date

#this function gets sunset time in Unix timestamps, ISO format, and date format 
def getSunset(city, country):
	observation = mgr.weather_at_place(city + ',' + country)
	weather = observation.weather
	sunset_unix = weather.sunset_time() # default unit: 'unix'
	sunset_iso = weather.sunset_time(timeformat='iso')
	sunset_date = weather.sunset_time(timeformat='date')
	
	return sunset_unix, sunset_iso, sunset_date

#This function gets visibility information at a certain distance in km and miles
def get_current_visibility(city, country):
	observation = mgr.weather_at_place(city + ',' + country)
	visibility = observation.weather.visibility_distance
	visibility_in_kms = observation.weather.visibility()
	visibility_in_miles = observation.weather.visibility(unit = 'miles')

	return visibility_in_kms, visibility_in_miles

#This function gets hourly temperatures information every 3-hours. 
def get_hourly_forecast(city, country):
	observation = mgr.weather_at_place(city + ',' + country)
	forecast = mgr.forecast_at_place(city + ',' + country, '3h').forecast

	#Creates an empty list to store values 
	hourly_temperatures = []

#Iterate through the hourly forecast data
	for weather in forecast:
		temperature = weather.temperature('fahrenheit')['temp'] #get temperatures
		hourly_temperatures.append(int(temperature)) #append to hourly_temperatures list

	return hourly_temperatures

#This function predicts wether it will rain tomorrow. 
def get_forecast_rain(city, country):
	#It uses the forecast_at_place method to obtain the 3-hour forecast and extracts the temperature for each hour.
	three_h_forecaster = mgr.forecast_at_place(city + ',' + country, '3h')
	tomorrow = timestamps.tomorrow()                   # datetime object for tomorrow
	rain_forecast = three_h_forecaster.will_be_rainy_at(tomorrow)

	return rain_forecast

#Thsi function gets air pollution information for a specified city. 
def get_air_pollution(city):
  air_mgr = owm.airpollution_manager()
  geolocator = Nominatim(user_agent="air_pollution_app")
  location = geolocator.geocode(city) #Geocodes the city

  if location:
    latitude, longitude = location.latitude, location.longitude #Get latitude and longitude of location
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    air_status = air_mgr.air_quality_forecast_at_coords(latitude, longitude) #gets air quality at those coords
    return air_status
  else:
  	return None

script_dir = os.path.dirname(os.path.abspath(__file__))
foldername = "static"
# File paths
csv_filename = "us-capitals.txt"
csv_file_path = os.path.join(script_dir, foldername, csv_filename)

#Opens the file with csv.DicReader
with open(csv_file_path, 'r', encoding='ISO-8859-1') as csvfile:

	records = []

	reader = csv.DictReader(csvfile)
	for row in reader: #Sore each row in the records list
		print(row)
		records.append(row)
 
#Define a rout '/map' for the Flask application  
@app.route("/map")
def display_map():
  #Initializes a Folium map centered at the United States with a specified zoom level
  mapObj = folium.Map(location=[39.83, -98.5795], zoom_start=4)
  #Iterates through the records and adds a marker for each capital on the Folium map
  for record in records:
  #Extract latitude ad longitude from each record
    latitude = float(record['latitude'])
    longitude = float(record['longitude'])
    coords = (latitude, longitude)
    folium.Marker(coords, tooltip=record['name'] + '<br>' + record['description']).add_to(mapObj)

  # set iframe width and height
  mapObj.get_root().width = "1300px"
  mapObj.get_root().height = "650px"

  # Creates an HTML content string representing the Folium map
  iframe = mapObj.get_root()._repr_html_()
  
  return render_template_string( #allows you to pass variables to the HTML template. 
      """
          <!DOCTYPE html>
          <html>
              <head></head>
              <body style = "background: linear-gradient(115deg, #56d8e4 10%, #9f01ea 90%); font-family: serif;">
                  <h1 style = "color:Purple; border-color: Black">US Capitals Map</h1>
                  {{ iframe|safe }}
              <input type="button" onclick="location.href=\'/\'" value="Start Again" />
              </body>
          </html>
      """,
      iframe=iframe,
  )
  #Start again button at the end of the HTML 

@app.route('/')
def main():
  html = ''
  html += '<!DOCTYPE html>'
  html += '<html>'
  html += '<head>'
  html += '<title>Form</title>'
  html += '</head>'
  html += '<body style = "background: linear-gradient(90deg, hsla(120, 93%, 84%, 1) 0%, hsla(185, 90%, 51%, 1) 100%);">'
  html += '<h1 style = "color: White; border: 0.5vh solid rgba(105, 195, 255, 0.8)" >Weather Insights: A Visual Exploration of Weather Patterns</h1>'
  html += f'<p style = "color: Blue">{dt_string_sf}</p>'
  html += '<hr>'
  html += '<p><strong>Providing fast weather forecast and nowcast.</strong></p>'
  html += '<img style ="border:5px double black; float:right" src="https://www.surfertoday.com/images/stories/political-world-map.jpg" width="1000" height="500">'
  html += '<br>'
  #Create a button to access the map 
  html += f'<a href="{url_for("display_map")}"><button>Show U.S. capitals Map</button></a>'
  html += '<br>'
  html += '<br>'
  
	#Current Weather Form
  html += '<form method="POST" action="form_input">'
  html += '<label for="weatherParameter">Select Weather Parameter:</label>'
  html += '<select name ="weatherParameter" id="weatherParameter">'
  html += '<option value="current">Current Weather</option>'
  html += '<option value="temperature">Temperature</option>'
  html += '<option value="wind">Wind</option>'
  html += '<option value="pressure">Pressure</option>'
  html += '<option value="rain">Rain</option>'
  html += '<option value="sunrise">Sunrise</option>'
  html += '<option value="sunset">Sunset</option>'
  html += '<option value="visibility">Visibility</option>'
  html += '</select>'
  html += '<br>'
  html += '<p>Select the city and country:</p>'
  html += 'City: <input type="text" class="submit-text" name="city" />\n'
  html += '<p>\n'
  html += 'Country: <input type="text" class="submit-text" name="country" />\n'
  html += '<input type="submit" class="submit-btn" value="Submit" />'
  html += '</p>'	
  html += '</form>\n'
  html += '<hr>'
  html += '<br>'

  #Second Weather Form 
  html += '<form method="POST" action="forecast_input">'
  html += '<label for="forecastParameter">Select Parameter:</label>'
  html += '<select name ="forecastParameter" id="forecastParameter">'
  html += '<option value="rain">Rain Tomorrow</option>'
  html += '<option value="pollution">Air Pollution</option>'
  html += '<br>'

  html += '</select>'
  html += '<br>'
  html += '<p>Select the city and country:</p>'
  html += 'City: <input type="text" class="submit-text" name="city" />\n'
  html += '<p>\n'
  html += 'Country: <input type="text" class="submit-text" name="country" />\n'
  html += '<input type="submit" class="submit-btn" value="Submit" />'
  html += '</p>'
  html += '</form>\n'

  html += '</body></html>'
  
  return html


@app.route('/form_input', methods=['POST'])
def form_input():
	#Extract the values of city and country submitted
	city = request.form['city']
	country = request.form['country']
	weather_parameter = request.form.get('weatherParameter')

	if not weather_parameter: #Input validation 
		return "Please select a weather paramenter."

	#Checks weather parameter value and calls corresponding functions to get and format weather info
	elif weather_parameter == 'current':
		current_weather = getCurrentWeather(city, country)
		result = f'The current weather status in {city} is {current_weather}. '
	elif weather_parameter == 'temperature':
		fahrenheit_temperature, celsius_temperature = getWeather(city, country)
		temperature_f = fahrenheit_temperature['temp'] #current temperature in fahrenheit
		temperature_c = celsius_temperature['temp'] #current temperature in celsius
		max_temperature_f = fahrenheit_temperature['temp_max'] #get the 'temp max' key in fahrenheit dictionary 
		min_temperature_f = fahrenheit_temperature['temp_min']
		max_temperature_c = celsius_temperature['temp_max'] #get the 'temp max' key in celsius dictionary 
		min_temperature_c = celsius_temperature['temp_min']
		feels_temperature_f = fahrenheit_temperature['feels_like'] 
		feels_temperature_c = celsius_temperature['feels_like']

		result = (
			f'The current temperature in {city} is {temperature_f}°F/ {temperature_c}°C.'
			f'The max temperature is {max_temperature_f}°F/ {max_temperature_c}°C.\n'
			f'The min temperature is {min_temperature_f}°F/ {min_temperature_c}°C.\n'
			f'Perceived temperature {feels_temperature_f}°F/ {feels_temperature_c}°C.'
			)

	elif weather_parameter == 'wind':
		wind_data = getWind(city, country)['speed']
		result = f'The wind speed in {city} is {wind_data} m/s'

	elif weather_parameter == "pressure":
		pressure_dict = getPressure(city, country)
		pressure = pressure_dict['press']
		pressure_sea_level = pressure_dict['sea_level']

		result = f"The atmospheric pressure in {city} is {pressure} hPa. The seal level pressure is {pressure_sea_level}."

	elif weather_parameter == "rain":
		rain_dict = getRain(city, country)
		rain_1h = rain_dict.get('1h',0) # Amount of rain fallen in the last 1 and 3 hours 
		rain_3h = rain_dict.get('3h',0)
		result = (f"The amount of rain in {city} in the last hour is: {rain_1h} mm."
					f"The amount of rain in {city} in the last 3 hours is: {rain_3h} mm." 
					)

	elif weather_parameter == "sunrise":
		sunrise_unix, sunrise_iso, sunrise_date = getSunrise(city, country)
		result = (f"Sunrise time in unix = {sunrise_unix}\nSunrise time in iso = {sunrise_iso}\nSunrise time in date = {sunrise_date}")

	elif weather_parameter == "sunset":
		sunset_unix, sunset_iso, sunset_date = getSunset(city, country)
		result = (f"Sunset time in unix = {sunset_unix}\nSunset time in iso = {sunset_iso}\nSunset time in date = {sunset_date}")

	elif weather_parameter == "visibility":
		visibility_in_kms, visibility_in_miles = get_current_visibility(city, country)
		result = f"Current visibility in kms: {visibility_in_kms}\nCurrent visibility in miles: {visibility_in_miles}"

	hourly_temperatures= get_hourly_forecast(city, country) #Get hourly temperature forecast data 

	#Plot forecast data and plots using Matplotlib 
	fig, ax = plt.subplots()
	ax.plot(hourly_temperatures)
	ax.set_title("Hourly forecast temperatures")
	ax.set_xlabel("Time (hours)")
	ax.set_ylabel("Temperature (°F)")
	ax.grid()

	# Use os.path to create an absolute path
	image_path = os.path.join(os.path.dirname(__file__), 'static/hourly_forecast.png')
    
	print(image_path)
	fig.savefig(image_path) #Save the graph to the 'image_path'

	#HTML response with weather information, images and hourly forecast graph 
	html = ''
	html += '<html>\n'
	html += '<body style = "background: linear-gradient(115deg, #56d8e4 10%, #9f01ea 90%); font-family: serif;">\n'
	html += '<img style ="border:5px double black; float:right" src="https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg?auto=compress&cs=tinysrgb&w=800" width="300" height="150"'
	html += '<hr>'
	html += '<br>'
	html += f'<p>{dt_string_sf}</p>' #Display current time and date in San Francisco 
	html += '<br>'
	html += f'<p>{result}</p>' #Display result 
	html += '<br>'

	#Start Again botton 
	#onclick="location.href='/' defines a JavaScript code to be executed when the button is clicked.
	#location.href property to set the URL to the main page
	html += '<input type="button" onclick="location.href=\'/\'" value="Start Again" />'
	html += '<hr><br>'

	html += f'<h3> Hourly forecast in {city}</h3> '
	html += '<br>'

	#Display in HTML the hourly forecast graph 
	html += f'<img style ="border:5px double black; float:right" src="/static/hourly_forecast.png" alt="Hourly Forecast Graph" width="750" height="400">'
	
	html += '<table border="1">\n' #open table 
	html += '<tr><th>Hour</th><th>Temperature (°F)</th><th>Celsius(°C)</th></tr>\n'
	for hour, temperature in enumerate(hourly_temperatures): #Looping through each hour in the list 
		forecast_time = now + timedelta(hours=3 * hour) #Calculates forecast time by adding multiple of 3 hours to current time because the list of temperatures is for every 3 hours 
		temperature_celsius = (temperature - 32) * (5/9) #converts temperature to celsius 
		temperature_celsius = int(temperature_celsius) #convert from string to int
		formatted_time = forecast_time.strftime("%H") #format forecast time displaying only the hour part with 'strftime' method 
		html += f'<tr><td>{formatted_time}</td><td>{temperature}</td><td>{temperature_celsius}</td></tr>\n' #Structure HTML table row with three columns: formatted time, temperature in Fahrenheit, and temperature in Celsius
	html += '</table>\n' #Closing table 

	html += '<img style ="border:5px double black; float:right" src = "https://images.unsplash.com/photo-1592210454359-9043f067919b?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8d2VhdGhlcnxlbnwwfHwwfHx8MA%3D%3D" width="300" height="150">'
	html += '<img style ="border:5px double black; float:left" src = "https://www.southernliving.com/thmb/APmZDoQ9oDZHExf6dubVDsvzz14=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-1383026300-c9979ab93b1b4571a3ef3b36ccf50bb4.jpg" width="300" height="150">'
	html += '<br>'
	html += '<hr>'
	html += '<br>'
	html += '</body>\n'
	html += '</html>\n'
	return html


# New route to handle forecast input
@app.route('/forecast_input', methods=['POST'])
def forecast_input():
	#Extract the values of city and country submitted
	city = request.form['city']
	country = request.form['country']
	forecast_parameter = request.form.get('forecastParameter')

	# Get the timestamp from the user input
	timestamp = request.form.get('timestamp')


	if not forecast_parameter: #input validation 
		return "Please select a forecast parameter."

	#Depending on the selected parameter it proceeds to get the data
	elif forecast_parameter == "rain": #Handling rain forecast
		rain_forecast = get_forecast_rain(city, country)
		result = f'<p>Tomorrow will rain in {city} : {rain_forecast}</p>'

	elif forecast_parameter == "pollution":	
		#Works for all cities except San Francisco 
		air_status_list = get_air_pollution(city)
		result = ""
		if air_status_list:
			#handle air pollution data
			air_status = air_status_list[0]

			# Accessing individual pollutant levels
			co_level = air_status.co
			no_level = air_status.no
			no2_level = air_status.no2
			o3_level = air_status.o3
			so2_level = air_status.so2
			pm2_5_level = air_status.pm2_5
			pm10_level = air_status.pm10
			nh3_level = air_status.nh3

			# Accessing overall Air Quality Index (AQI)
			aqi_value = air_status.aqi
			#Displaing data in a table 
			result += (
				f"Air Status:"
		    f"<table border='1'>" #creates a table 
		    f"<tr><th>Levels of</th><th>Status</th></tr>"
		    f"<tr><td>CO</td><td>{co_level}</td></tr>"
		    f"<tr><td>NO</td><td>{no_level}</td></tr>"
		    f"<tr><td>NO2</td><td>{no2_level}</td></tr>"
		    f"<tr><td>O3</td><td>{o3_level}</td></tr>"
		    f"<tr><td>SO2</td><td>{so2_level}</td></tr>"
		    f"<tr><td>PM10</td><td>{pm10_level}</td></tr>"
		    f"<tr><td>NH3</td><td>{nh3_level}</td></tr>"
		    f"<tr><td>AQI</td><td>{aqi_value}</td></tr>"
		    f"</table>"
				)

		else: #error validation 
			result = "Could not fetch air pollution forecast."

	html = ''
	html += '<html>\n'
	html += '<body style="background: style = "background: linear-gradient(115deg, #56d8e4 10%, #9f01ea 90%); font-family: serif;">\n'
	html += '<img style ="border:5px double black; float:right" src="https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg?auto=compress&cs=tinysrgb&w=800" width="300" height="150"'
	html += '<hr>'
	html += '<br>'
	html += f'<p>{dt_string_sf}</p>'
	html += '<br>'
	html += f'<p>{result}</p>'
	html += '<br>'
	#Start Again button 
	html += '<input type="button" onclick="location.href=\'/\'" value="Start Again" />'
	html += '<hr><br>'
	html += '</body>\n'
	html += '</html>\n'
	return html

if __name__ == '__main__':
	app.run(debug=True)
