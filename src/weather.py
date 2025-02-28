import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Set up API and configurations
API_KEY = "9b76dc53d67c83af7eba09a2242645c7"
st.set_page_config(page_title="NDMA Weather", layout="wide")

# Dashboard header
st.title("🌤️ NDMA Current and 5 Day Weather")
st.markdown("---")

# Sidebar for city input
with st.sidebar:
    st.header("Configuration")
    city = st.text_input("Enter City Name", "Islamabad")
    units = st.selectbox("Select Units", ("metric", "imperial"))

# Main dashboard area
if city:
    try:
        # Fetch weather data
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Process data
        forecast_data = []
        for forecast in data['list']:
            forecast_data.append({
                'datetime': forecast['dt_txt'],
                'temperature': forecast['main']['temp'],
                'feels_like': forecast['main']['feels_like'],
                'humidity': forecast['main']['humidity'],
                'pressure': forecast['main']['pressure'],
                'wind_speed': forecast['wind']['speed'],
                'weather': forecast['weather'][0]['main'],
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon'],
                'visibility': forecast['visibility'],
                'clouds': forecast['clouds']['all'],
                'wind direction': forecast['wind']['deg'],
                "wind gust": forecast['wind']['gust'],
                
            })
        
        df = pd.DataFrame(forecast_data)
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Current weather
        current = df.iloc[0]
        unit_symbol = '°C' if units == 'metric' else '°F'
        
        # Display current weather
        st.header(f"Current Weather in {city}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image(f"http://openweathermap.org/img/wn/{current['icon']}@4x.png", width=150)
            st.markdown(f"**{current['description'].title()}**")
        with col2:
            st.image(f"high-temperature.png", width=110)
            st.metric("Temperature", f"{current['temperature']}{unit_symbol}", 
                     f"Feels like {current['feels_like']}{unit_symbol}")
        with col3:
            st.metric("Humidity", f"{current['humidity']}%")
            st.metric("Pressure", f"{current['pressure']} hPa")
        with col4:
            st.metric("Wind Speed", f"{current['wind_speed']} {'m/s' if units == 'metric' else 'mph'}")
        
        # Forecast visualizations
        st.markdown("---")
        st.header("5-Day Forecast")
        
        # Temperature chart
        fig_temp = px.line(df, x='datetime', y='temperature', 
                          labels={'temperature': f'Temperature ({unit_symbol})'},
                          title='Temperature Forecast')
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Humidity and Wind charts
        col1, col2 = st.columns(2)
        with col1:
            fig_humidity = px.area(df, x='datetime', y='humidity',
                                  labels={'humidity': 'Humidity (%)'},
                                  title='Humidity Forecast')
            st.plotly_chart(fig_humidity, use_container_width=True)
        
        with col2:
            fig_wind = px.bar(df, x='datetime', y='wind_speed',
                             labels={'wind_speed': f"Wind Speed ({'m/s' if units == 'metric' else 'mph'})"},
                             title='Wind Speed Forecast')
            st.plotly_chart(fig_wind, use_container_width=True)
        
        # Raw data table
        st.markdown("### Detailed Forecast Data")
        st.dataframe(df.style.format({
            'temperature': '{:.1f}' + unit_symbol,
            'feels_like': '{:.1f}' + unit_symbol,
            'humidity': '{:.0f}%',
            'pressure': '{:.0f} hPa',
            'wind_speed': '{:.1f} ' + ('m/s' if units == 'metric' else 'mph'),
            "wind direction": '{:.0f}°',
            "wind gust": '{:.1f} ' + ('m/s' if units == 'metric' else 'mph'),
            "visibility": '{:.0f} km',
            "clouds": '{:.0f}%',
            "datetime": '{:%Y-%m-%d %H:%M:%S}'
            
        }), use_container_width=True)
    
    except requests.exceptions.HTTPError as e:
        st.error(f"Error fetching data: {str(e)}")
    except KeyError:
        st.error("Invalid data received from API")