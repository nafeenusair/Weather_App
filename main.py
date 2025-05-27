import sys
import requests
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QLabel,
                             QPushButton, QWidget, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self.get_weather_button = QPushButton("Get Weather", self)
        self.enter_city_name = QLineEdit(self)
        self.city_name = QLabel("Enter city name: ", self)
        self.weather = QLabel(self)
        self.weather_emoji = QLabel(self)
        self.weather_condition = QLabel(self)
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("icon/weather.png"))

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.enter_city_name)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.weather)
        vbox.addWidget(self.weather_emoji)
        vbox.addWidget(self.weather_condition)
        self.setLayout(vbox)

        self.city_name.setAlignment(Qt.AlignCenter)
        self.enter_city_name.setAlignment(Qt.AlignCenter)
        self.weather.setAlignment(Qt.AlignCenter)
        self.weather_emoji.setAlignment(Qt.AlignCenter)
        self.weather_condition.setAlignment(Qt.AlignCenter)

        self.city_name.setObjectName("city_name")
        self.enter_city_name.setObjectName("enter_city_name")
        self.weather.setObjectName("weather")
        self.weather_emoji.setObjectName("weather_emoji")
        self.weather_condition.setObjectName("weather_condition")
        self.get_weather_button.setObjectName("get_weather_button")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
                font-weight: bold;
            }
            
            QLabel#city_name{
                font-size: 40px;
                font-style: italic;
                font-weight: normal;
            }
            
            QLineEdit#enter_city_name{
                font-size: 20px;
            }
            
            QPushButton#get_weather_button{
                font-size: 20px;
                background-color: #d5d5db;
            }
            
            QLabel#weather{
                font-size: 35px;
            }
            
            QLabel#weather_condition{
                font-size: 35px;
                font-weight: normal;
            }
            
            QLabel#weather_emoji{
                font-size: 90px;
                font-family: Segoe UI emoji;
            }  
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "73abab08ef73adb8d6cfdd257752126e"
        city = self.enter_city_name.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Error: 400 Bad Request\nPlease check your input.")
                case 401:
                    self.display_error("Error: 401 Unauthorized\nAuthentication is required or failed.")
                case 403:
                    self.display_error("Error: 403 Forbidden\nYou do not have permission to access this resource.")
                case 404:
                    self.display_error("Error: 404 Not Found\nThe requested city could not be found.")
                case 500:
                    self.display_error("Error: 500 Internal Server Error\nThe server encountered an error.")
                case 501:
                    self.display_error("Error: 501 Not Implemented\nThe server does not support the request.")
                case 502:
                    self.display_error("Error: 502 Bad Gateway\nInvalid response from the upstream server.")
                case 504:
                    self.display_error("Error: 504 Gateway Timeout\nThe server did not receive a timely response.")
                case _:
                    self.display_error(f"{http_error} Unknown Error\nPlease try again later.")


        except requests.exceptions.ConnectionError:
            self.display_error("No Internet\nCheck your internet connection and try again!")
        except requests.exceptions.Timeout:
            self.display_error("Request Timed Out\nThe server took too long to respond.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\nCheck the URL and try again.")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"An unexpected error occurred:\n{req_error}")

    def display_error(self, message):
        self.weather.setStyleSheet("font-size: 18px;")
        self.weather.setText(message)
        self.weather_emoji.clear()
        self.weather_condition.clear()

    def display_weather(self, data):
        self.weather.setStyleSheet("font-size: 75px")
        tem_k = data["main"]["temp"]
        tem_c = tem_k - 273.15
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.weather.setText(f"{tem_c:.0f}°C")
        self.weather_emoji.setText(self.get_weather_emoji(weather_id))
        self.weather_condition.setText(f"{weather_description}")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 761:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

def main():
    app = QApplication(sys.argv)
    weather = Weather()
    weather.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()