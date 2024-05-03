# Description: This script sends an email reminder to take an umbrella if the weather is rainy or cloudy in Srinagar.
#Author: Wilayat Ali Kawoosa, Fatima Shah & Tajeshwar Singh
#Date: 10th October 2021 
#The liberary used in this script are: smtplib, schedule, requests, BeautifulSoup, time

import smtplib # Importing the smtplib library for sending emails
import schedule # Importing the schedule library for scheduling the reminder
import requests # Importing the requests library for making HTTP requests
from bs4 import BeautifulSoup # Importing the BeautifulSoup library for web scraping
import time # Importing the time library for adding delays

def sendReadyEmail(): # Function to send a ready email
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.starttls()
        
        email = "weather.appdpsb@gmail.com"
        password = "fsyo uakf vhvx tyuu"  # Get password from environment variable
        smtp_object.login(email, password)
        
        subject = "Script Ready"
        body = "Ready"
        msg = f"Subject:{subject}\n\n{body}\n\nRegards,\nDPSB Weather App"
        
        smtp_object.sendmail(email, "ayaanasrar3473@gmail.com", msg)
        print("Ready email sent!")
    except Exception as e:
        print(f"An error occurred while sending the ready email: {e}")
    finally:
        if 'smtp_object' in locals():
            smtp_object.quit()

def umbrellaReminder(): 
    city = "Srinagar"
    
    url = "https://www.google.com/search?q=weather+" + city 
    
    html = requests.get(url).content 
    
    soup = BeautifulSoup(html, 'html.parser') 
    temperature = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text 
    time_sky = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text 
    
    sky = time_sky.split('\n')[1] 
    
    print("Sky:", sky)
    print("Temperature:", temperature)

    if sky in ["Rainy", "Rain And Snow", "Showers", "Haze", "Cloudy"]: 
        smtp_object = None  # Initialize smtp_object outside the try block
        try:
            smtp_object = smtplib.SMTP('smtp.gmail.com', 587) 
            smtp_object.starttls() 
            email = "weather.appdpsb@gmail.com"
            password = "fsyo uakf vhvx tyuu"  # get password from environment variable
            smtp_object.login(email, password)
            
            subject = "Umbrella Reminder"
            body = f"Take an umbrella before leaving the house. Weather condition for today is {sky} and temperature is {temperature}°C in {city}."
            msg = f"Subject:{subject}\n\n{body}\n\nRegards,\nDPSB Weather App".encode('utf-8')
            
            smtp_object.sendmail(email, "ayaanasrar3473@gmail.com", msg)
            print("Email Sent!")  # Add this line for confirmation
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
        finally:
            if smtp_object:
                smtp_object.quit()

# Send "Ready" email
sendReadyEmail()

# Send weather update
umbrellaReminder()

# Schedule the reminder to run at 6:00 AM every day
schedule.every().day.at("06:00").do(umbrellaReminder)

# Loop to keep the script running indefinitely
while True: 
    schedule.run_pending()
    time.sleep(60)  # Check for pending tasks every 60 seconds