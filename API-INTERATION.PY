pip install matplotlib seaborn
pip install dash
import requests
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
# Step 1: Fetch data from API
api_key = "33e708512f951aa185cf3fb437775d79"  # Replace with your API key
city = "Hyderabad"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse JSON response
    print("Data fetched successfully!")
else:
    print("Error:", response.status_code)
    exit()  # Stop execution if the API request fails

# Step 2: Process data
temperature = data['main']['temp']
humidity = data['main']['humidity']
weather_description = data['weather'][0]['description']
wind_speed = data['wind']['speed']
pressure = data['main']['pressure']

# Step 3: Store data in DataFrame
weather_data = {
    "City": [city],
    "Temperature (°C)": [temperature],
    "Humidity (%)": [humidity],
    "Weather": [weather_description],
    "Wind Speed (m/s)": [wind_speed],
    "Pressure (hPa)": [pressure]
}
df = pd.DataFrame(weather_data)

# Step 4: Reshape data for visualization
metrics = df.columns[1:].tolist()  # All metrics except "City"
values = df.iloc[0, 1:].tolist()   # All values except "City"

# Create a new DataFrame for visualization
viz_df = pd.DataFrame({
    "Metrics": metrics,
    "Values": values
})

# Step 5: Create a Dash app
app = Dash(__name__)

# Create a bar chart using Plotly Express
bar_fig = px.bar(viz_df, x="Metrics", y="Values",
                 labels={"x": "Metrics", "y": "Values"},
                 title=f"Weather Metrics in {city}")

# Create a pie chart for weather conditions
pie_fig = px.pie(names=["Temperature", "Humidity", "Wind Speed", "Pressure"],
                 values=[temperature, humidity, wind_speed, pressure],
                 title=f"Weather Distribution in {city}")

# Create a scatter plot to show the relationship between temperature and humidity
scatter_fig = px.scatter(df, x="Temperature (°C)", y="Humidity (%)",
                         title=f"Temperature vs Humidity in {city}",
                         labels={"x": "Temperature (°C)", "y": "Humidity (%)"})

# Layout of the app
app.layout = html.Div(children=[
    html.H1(children="Weather Dashboard"),

    # Bar Chart
    dcc.Graph(figure=bar_fig),

    # Pie Chart
    dcc.Graph(figure=pie_fig),

    # Scatter Plot
    dcc.Graph(figure=scatter_fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
  
