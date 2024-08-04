import requests
from .. import loader, utils

class WeatherModule(loader.Module):
    """Показывает погоду в указанном городе"""
    strings = {
        "name": "Weather",
        "no_city": "❗ Пожалуйста, укажите название города.",
        "fetch_error": "❗ Не удалось получить данные о погоде. Проверьте название города и попробуйте снова."
    }

    def __init__(self):
        self.config = loader.ModuleConfig("API_KEY", "a02c91969383c2bd1cf56a292977f67b", lambda m: "Ваш API ключ от OpenWeatherMap")

    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.config['API_KEY']}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            return weather
        else:
            return None

    @loader.command()
    async def weathercmd(self, message):
        """Показывает погоду в указанном городе"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_city"])
            return

        city = args
        weather = self.get_weather(city)

        if weather:
            reply = (
                f"🌆 Погода в {weather['city']}:\n"
                f"🌡️ Температура: {weather['temperature']}°C\n"
                f"🌤️ Описание: {weather['description']}\n"
                f"💧 Влажность: {weather['humidity']}%\n"
                f"💨 Скорость ветра: {weather['wind_speed']} м/с"
            )
        else:
            reply = self.strings["fetch_error"]

        await utils.answer(message, reply)