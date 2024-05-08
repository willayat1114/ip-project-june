#version: 1.0.a
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def get_user_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        return data.get('city')  # Extract the city from the response data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user location: {e}")
        return None

def get_weather(api_key, city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def send_email(weather_condition, recipient_email):
    # Email configuration
    sender_email = "weather.appdpsb@gmail.com"
    sender_password = "fsyo uakf vhvx tyuu"

    # Compose email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    
    # Update email subject based on weather condition
    if "clear" in weather_condition.lower():
        message['Subject'] = "Clear Sky Weather Alert"
    elif "cloudy" in weather_condition.lower() or "rain" in weather_condition.lower() or "snow" in weather_condition.lower():
        message['Subject'] = f"{weather_condition.capitalize()} Weather Alert"
    else:
        message['Subject'] = "Weather Alert"

    # Compose email body based on weather condition
    if "clear" in weather_condition.lower():
        body = "Hey there!\n\nThe sky is clear today. It's a great day for running, cycling, or a picnic!\n\nEnjoy the weather!"
    elif "cloudy" in weather_condition.lower() or "rain" in weather_condition.lower() or "snow" in weather_condition.lower():
        body = f"Hey there!\n\nIt's {weather_condition} today. You should take an umbrella when you go out.\n\nStay dry!"
    else:
        body = f"Hey there!\n\nThe weather today is {weather_condition}. Enjoy your day!\n\nBest regards,"

    message.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
    print("Email sent successfully!")

def main():
    api_key = "12eaadc2dbd0425a95850228240805"  # Replace this with your actual WeatherAPI key
    recipient_email = "ayaanasrar3473@gmail.com"  # Replace this with the recipient's email

    user_location = get_user_location()
    if user_location:
        print(f"Detecting weather for {user_location}...")
        weather_data = get_weather(api_key, user_location)
        if weather_data:
            current = weather_data['current']
            condition = current['condition']['text']
            temperature = current['temp_c']
            humidity = current['humidity']
            observation_time = current['last_updated']

            # Convert observation time to datetime object
            observation_time = datetime.datetime.strptime(observation_time, '%Y-%m-%d %H:%M')
            
            print(f"Weather in {user_location}:")
            print(f"Condition: {condition}")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Time of observation: {observation_time.strftime('%Y-%m-%d %H:%M')}")

            # Send email notification based on weather condition
            send_email(condition, recipient_email)
        else:
            print("Unable to fetch weather data.")
    else:
        print("Unable to detect user location. Please enter a city name manually.")

if __name__ == "__main__":
    main()
