"""meteo_API for X days."""


def get_wind_direct(degrees) -> str:
    """Pass."""
    winddirections = (
        'северный',
        'северо-восточный',
        'восточный',
        'юго-восточный',
        'южный',
        'юго-западный',
        'западный',
        'северо-западный'
    )
    index = int((degrees + 22.5) // 45 % 8)
    return winddirections[index]


def get_data(today=True) -> dict:
    """pass."""
    import openmeteo_requests

    import requests_cache
    import pandas as pd
    from retry_requests import retry
    from datetime import datetime

    cache_session = requests_cache.CachedSession(
        '.cache',
        expire_after=3600
    )
    retry_session = retry(
        cache_session,
        retries=5,
        backoff_factor=0.2
    )
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important
    # to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.8467,
        "longitude": 37.3586,
        "wind_speed_unit": "ms",
        "current": [
            "temperature_2m", "relative_humidity_2m",
            "apparent_temperature", "is_day", "precipitation",
            "rain", "showers", "snowfall", "wind_speed_10m",
            "wind_direction_10m", "wind_gusts_10m"
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "apparent_temperature_max", "apparent_temperature_min",
            "sunrise", "sunset", "daylight_duration", "sunshine_duration",
            "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum",
            "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours",
            "precipitation_probability_max", "wind_speed_10m_max",
            "wind_gusts_10m_max", "wind_direction_10m_dominant",
            "shortwave_radiation_sum", "et0_fao_evapotranspiration"
        ],
        "timezone": "Europe/Moscow"
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()

    current_time = (
        datetime.fromtimestamp(current.Time()).strftime('%d.%m.%Y %H:%M')
    )

    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    # current_apparent_temperature = current.Variables(2).Value()
    # current_is_day = current.Variables(3).Value()
    current_precipitation = current.Variables(4).Value()
    # current_rain = current.Variables(5).Value()
    # current_showers = current.Variables(6).Value()
    # current_snowfall = current.Variables(7).Value()
    current_wind_speed_10m = current.Variables(8).Value()
    current_wind_direction_10m = current.Variables(9).Value()
    # current_wind_gusts_10m = current.Variables(10).Value()

    # Process daily data. The order of variables
    # needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
    daily_sunrise = daily.Variables(5).ValuesAsNumpy()
    daily_sunset = daily.Variables(6).ValuesAsNumpy()
    daily_daylight_duration = daily.Variables(7).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(8).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(9).ValuesAsNumpy()
    daily_uv_index_clear_sky_max = daily.Variables(10).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(11).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(12).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(13).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(14).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(15).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(16).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(17).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(18).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(19).ValuesAsNumpy()
    daily_shortwave_radiation_sum = daily.Variables(20).ValuesAsNumpy()
    daily_et0_fao_evapotranspiration = daily.Variables(21).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["sunrise"] = daily_sunrise
    daily_data["sunset"] = daily_sunset
    daily_data["daylight_duration"] = daily_daylight_duration
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["uv_index_max"] = daily_uv_index_max
    daily_data["uv_index_clear_sky_max"] = daily_uv_index_clear_sky_max
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["precipitation_hours"] = daily_precipitation_hours
    daily_data["precipitation_probability_max"] = (
        daily_precipitation_probability_max
        )
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
    daily_data["wind_direction_10m_dominant"] = (
        daily_wind_direction_10m_dominant
        )
    daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
    daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration

    # daily_dataframe = pd.DataFrame(data=daily_data)

    # custom points:
    # today_date = daily_data['date'][1]
    # tomorrow_date = daily_data['date'][2]

    # tomorrow wind
    tomorrow_wind = daily_wind_speed_10m_max[2]
    tomorrow_wind_direction = daily_wind_direction_10m_dominant[2]

    # temperatures
    current_temperature = int(current_temperature_2m)
    today_temperature_max = int(daily_temperature_2m_max[1])
    today_temperature_min = int(daily_temperature_2m_min[1])

    tomorrow_temperature_max = int(daily_temperature_2m_max[2])
    tomorrow_temperature_min = int(daily_temperature_2m_min[2])

    # showers and rain
    current_precip = int(current_precipitation)
    today_precip = int(daily_precipitation_probability_max[1])
    tomorrow_precip = int(daily_precipitation_probability_max[2])
    tomorrow_precip = int(daily_precipitation_probability_max[2])

    if today:
        return {
            'min_temp': today_temperature_min,
            'max_temp': today_temperature_max,
            'cur_precip': current_precip,
            'precip_prob': today_precip,
            'cur_temp': current_temperature,
            'wind': current_wind_speed_10m,
            'wind_direct': get_wind_direct(current_wind_direction_10m),
            'humid': current_relative_humidity_2m,
            'time': current_time,
        }
    return {
        'min_temp': tomorrow_temperature_min,
        'max_temp': tomorrow_temperature_max,
        'precip_prob': tomorrow_precip,
        'wind': tomorrow_wind,
        'wind_direct': get_wind_direct(tomorrow_wind_direction),
    }
