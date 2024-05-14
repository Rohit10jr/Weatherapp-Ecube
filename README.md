# WeatherNow - Your Personal Weather Dashboard
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

Welcome to WeatherNow, a super cool Django weather app that provides you with real-time weather data for your favorite cities along with a historical data feature for the past two weeks. 
With WeatherNow, you can stay informed about the weather conditions of your preferred locations, helping you plan your activities accordingly.

## Features:

Real-time Weather Data: WeatherNow fetches real-time weather information from reliable sources to provide you with accurate and up-to-date weather details for your chosen cities.

Favorite Cities: You can add your favorite cities to the dashboard and easily switch between them to check their current weather conditions.

Two Weeks Historical Data: WeatherNow not only gives you current weather updates but also allows you to access historical weather data for the past two weeks, including temperature and humidity trends.

User-friendly Interface: The app is designed with a user-friendly interface, making it easy to navigate and obtain the desired weather information effortlessly.

## How to Use:

Signup/Login: Create an account or log in to your existing account to access the dashboard.

Add Cities: Add your favorite cities to the dashboard by searching for them and clicking on the 'Add' button.

View Current Weather: Once your cities are added, you can view their current weather conditions on the dashboard.

Access Historical Data: Navigate to the historical data section to explore the temperature and humidity trends for the past two weeks.

Edit or Remove Cities: You can edit or remove cities from your dashboard as per your preference.

## Technologies Used:

Django: The web framework used for developing the application.
OpenWeather API: To fetch real-time and historical weather data.
HTML/CSS: For frontend development and styling.
PostgreSQL: Database management system for storing user data and weather information.

## Installation:

Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/weathernow.git
Install dependencies:
Copy code
pip install -r requirements.txt
Set up your PostgreSQL database and update the database settings in settings.py accordingly.

Apply migrations:

Copy code
python manage.py migrate
Run the server:
Copy code
python manage.py runserver
Access the application at http://localhost:8000/ in your web browser.

## Contributing:

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, feel free to open an issue or submit a pull request.

License:

This project is licensed under the MIT License - see the LICENSE file for details.

Contact:

For any inquiries or support, please contact your.email@example.com.

Enjoy using WeatherNow and stay updated with the weather conditions of your favorite cities!
