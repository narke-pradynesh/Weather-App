import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class myApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.city_name = QLabel("Enter city: ", self)       # Created input method for City Name
        self.name_plcholder = QLineEdit(self)
        self.get_button = QPushButton("Get Weather",self)
        self.temp = QLabel( self)
        self.symbol = QLabel( self)
        self.description = QLabel(self)
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Weather")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_name)
        vbox.addWidget(self.name_plcholder)
        vbox.addWidget(self.get_button)
        vbox.addWidget( self.temp)
        vbox.addWidget(self.symbol)
        vbox.addWidget(self.description)

        self.setLayout(vbox)

        self.city_name.setAlignment(Qt.AlignCenter)
        self.name_plcholder.setAlignment(Qt.AlignCenter)
        self.temp.setAlignment(Qt.AlignCenter)
        self.symbol.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)

        # Setting Object Names for CSS formatting
        self.city_name.setObjectName("city_name")
        self.name_plcholder.setObjectName("name_plcholder")
        self.get_button.setObjectName("get_button")
        self.temp.setObjectName("temp")
        self.symbol.setObjectName("symbol")
        self.description.setObjectName("description")

        # CSS Properties for Objects
        self.setStyleSheet('''
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_name{
                font-size: 100px;
                font-style: italic;
            }
            QLineEdit#name_plcholder{
                font-size: 110px;
            }
            QPushButton#get_button{
                font-size: 60px;
                font-weight: bold;
            }
            QLabel#temp{
                font-size: 140px;
            }
            QLabel#symbol{
                font-size: 150px;
                font-family: Segoe UI emoji;
            }
            QLabel#description{
                font-size: 100px;
            }
        ''')
        self.get_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "c9fc515c85a7ddcbb937624b5d914171"
        city = self.name_plcholder.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    # Success and Error Case Handling
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:     
            match response.status_code:
                case 400:
                   self.display_error()
                case 401:
                    self.display_error("Unauthorised\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("City not found")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from service")
                case 503:
                    self.display_error("Service Unavailale\nServer Down")
                case 504:
                    self.display_error("Gateway Timeout\nNo Response from Server")
                case _:
                    self.display_error(f"Http Error Occured: {http_error}")

            
        except requests.exceptions.RequestException:
            pass
            

    def display_error(self, message):
        self.temp.setStyleSheet("font-size: 60px;")
        self.temp.setText(message)
        self.symbol.clear()
        self.description.clear()

    def display_weather(self,data):
        self.temp.setStyleSheet("font-size: 140px;")
        temp_c = data["main"]["temp"] - 273.15
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temp.setText(f"{temp_c:.1f}°C")
        self.symbol.setText(self.get_emoji(weather_id))
        self.description.setText(f"{weather_description}")
    
    @staticmethod
    def get_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801<= weather_id <= 804:
            return "☁️"
        else:
            return " " 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = myApplication()
    weather_app.show()
    sys.exit(app.exec_())