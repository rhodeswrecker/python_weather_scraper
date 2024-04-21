import schedule 
import smtplib    
import requests 
from bs4 import BeautifulSoup 
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values

def weather_reminder(): 
    load_dotenv() 
    city = "Cleveland%2C+OH"
    url = "https://www.google.com/search?q=" + city + "+weather+tomorrow"
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    forecast = soup.find( 'div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text 

    #formatting the data
    day = forecast.split('\n')[0]
    weather = forecast.split('\n')[1]
    temps = forecast.split('\n')[2]

    subject_line = "Daily Weather Forecast for " + day
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587) 
    
    # start TLS for security 
    smtp_object.starttls()
    smtp_object.login(os.getenv("Email"), os.getenv("Password"))

    subject_line = "Daily Weather Forecast for " + day
    weather_prognosis = ""
    if(weather != "Sunny" and weather != "Partly Cloud" and weather != "Haze"):
        weather_prognosis = f"Sadly, due to the lake right next to us, Cleveland has once again descended into a\nmorose weather situation that will be course corrected at the nearest high pressure front.\nThe particular weather tomorrow will be {weather}."
    else:
        weather_prognosis = "Our good behavior at Browns and Guardians games has paid off and God has gifted us \nwith a rare good weather forecast. Let us enjoy it and head on down to Edgewater."
    main_body = f"The temperature of {day} will be {temps} with the weather prognosis as follows: \n{weather_prognosis}"

    msg = f"Subject:{subject_line}\n\n{main_body}\nRegards, Harrison Rhodes" 
    msg = msg.encode('utf-8') 
    smtp_object.sendmail(os.getenv("Email"), 
                        os.getenv("Email"), msg) 
    smtp_object.quit() 
    print("Email Sent!")

schedule.every().day.at("19:14").do(weather_reminder)
  
while True: 
    schedule.run_pending() 
