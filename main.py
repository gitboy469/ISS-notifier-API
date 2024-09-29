# Import necessary libraries
import requests  # Used to make HTTP requests to get ISS and sunset/sunrise data
from datetime import datetime  # Used to handle date and time-related tasks
import smtplib  # Used to send emails
import time  # Used to add delays in the execution of the program

# Define email addresses and password
to_address = "your address"  # Recipient email address
from_address = "your address"  # Sender email address (could be the same as recipient)
MY_PASSWORD = "fghffcvfgfccv"  # Email account password

# Define your geographic location (latitude and longitude)
MY_LAT = 4891177  # Replace with your actual latitude
MY_LONG = 3300726  # Replace with your actual longitude

# Function to check if the ISS is currently overhead
def is_iss_overhead():
    # Make a GET request to the ISS API to get the current position of the ISS
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()  # Raise an error if the request was unsuccessful

    # Parse the JSON response to get the ISS latitude and longitude
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Check if the ISS is within a +/- 5-degree range of your location
    if (MY_LAT-5) <= iss_latitude <= (MY_LAT+5) and (MY_LONG-5) <= iss_longitude <= (MY_LONG+5):
        return True  # Return True if the ISS is overhead

# Function to check if it is currently nighttime at your location
def is_night():
    # Define parameters for the sunrise-sunset API (your location)
    parameters = {
        "lat": MY_LAT,  # Your latitude
        "lng": MY_LONG,  # Your longitude
        "formatted": 0,  # Get the time in 24-hour format (UTC)
    }

    # Make a GET request to the sunrise-sunset API to get sunrise and sunset times
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()  # Raise an error if the request was unsuccessful

    # Parse the JSON response to get sunrise and sunset times
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])  # Extract the hour of sunrise
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])  # Extract the hour of sunset

    # Get the current hour in UTC
    time_now = datetime.now().hour

    # Check if the current time is after sunset or before sunrise (i.e., it's nighttime)
    if time_now >= sunset or time_now <= sunrise:
        return True  # Return True if it's nighttime

# Main loop that runs indefinitely
while True:
    time.sleep(60)  # Wait for 60 seconds before running the checks again

    # If the ISS is overhead and it is nighttime, send an email notification
    if is_iss_overhead() and is_night():
        # Create a secure connection to the SMTP server using SSL
        connection = smtplib.SMTP_SSL("smtp.gmail.com", port=465)
        try:
            # Log in to the email account
            connection.login(to_address, MY_PASSWORD)

            # Send an email notification
            connection.sendmail(
                from_addr=from_address,
                to_addrs=to_address,
                msg="Subject:Look Up \n\nThe ISS is above you in the sky."  # Email subject and body
            )
            print("Email sent successfully!")  # Print confirmation message
        except Exception as e:
            # Print an error message if the email fails to send
            print(f"Failed to send email: {e}")
        finally:
            # Close the connection to the SMTP server
            connection.quit()
