# Weather-App

https://quilled-gray-lungfish.glitch.me/

This project is a Flask web application that provides real-time weather data and visual insights. Users can check the current weather, forecast details, and explore U.S. capital cities on an interactive map. The application leverages `OpenWeatherMap API` and visualizes data using `Folium`, `Matplotlib`, and `Geop`y.

API: Open Weather Map: Weather Service https://openweathermap.org/

OpenWeather is a comprehensive weather API that offers a wide range of weather data, including current conditions, recasts, historical data, and more. It provides various weather parameters, such as temperature, humidity, wind speed, and precipitation. 

**Features**
- Utilize OpenWeather API to retrieve diverse weather parameters(temperature, humidity, wind speed, precipitation)
- Use `HTML`, `CSS`, and `Python` to structure and style the web application. 
- Ask the user for input. This could involve allowing users to select specific locations, time frames, or weather parameters they are interested in. 
- Use of libraries like `matplotlib` or `plotly` to create graphs and maps illustrating weather patterns. 
- Use graphical context in maps to illustrate variations effectively. Ensure the user interface is intuitive. 
- Save the generated maps to an HTML file to enable the user to revisit and share specific visualizations.

**Prerequisites** 

Make sure you have the following installed:

1. Python 3.7+
2.Virtual environment (optional but recommended)

**Required Python Libraries**
You can install the required libraries by running:
`pip install -r requirements.txt`

Here’s the list of key libraries used:
- `Flask`: For creating the web application
- `pyowm`: For accessing weather data from the OpenWeatherMap API
- `folium`: For displaying an interactive map of U.S. capital cities
- `geopy`: For geocoding city locations
- `matplotlib`: For plotting forecast weather data
- `csv`: For parsing U.S. capital data

Create a `requirements.txt file` and add the following lines:
Flask
pyowm
folium
geopy
matplotlib

**Setup and Running the Application**
1. Clone the repository: Clone this repository to your local machine using:
   `git clone <repository_url>`
2. Install dependencies: Navigate to the project directory and install the dependencies:
  `pip install -r requirements.txt`
3. Set up the OpenWeatherMap API: Get your free API key from the OpenWeatherMap website.
4. Configure the API key: Open the app.py file and replace  `0e884fdc78cdf0265beca2ced044fbeb` with your own OpenWeatherMap API key in the following line:
  `owm = OWM('your_api_key_here')`
5. Run the application: After configuring the API key, start the Flask development server by running the following command:
     `python app.py`
6. Access the web application: Open your web browser and navigate to:
   `http://127.0.0.1:5000/`

**Usage**
- Weather Data: Enter a city and country, and select a weather parameter to get detailed weather information.
- Forecast: Get predictions for rain tomorrow or air pollution levels for a specific city.
- Map Visualization: Click on "Show U.S. capitals Map" to explore U.S. capitals with weather data displayed as tooltips.









