COLUMN_NAMES = ["Date",
    "Daily Mean Temperature (0900-0900) (°C)",
    "Daily Total Rainfall (0900-0900) (mm)",
    "Daily Total Sunshine (0000-2400) (hrs)",
    "Daily Mean Windspeed (0000-2400) (kn)",
    "Daily Mean Windspeed (0000-2400) (Beaufort conversion)",
    "Daily Maximum Gust (0000-2400) (kn)",
    "Daily Maximum Relative Humidity (%)",
    "Daily Mean Total Cloud (oktas)",
    "Daily Mean Visibility (dam)",
    "Daily Mean Pressure (hPa)",
    "Daily Mean Wind Direction (deg)",
    "Cardinal Direction (Mean)",
    "Daily Max Gust Corresponding Direction (deg)",
    "Cardinal Direction (Max)"]
"""Array containing the column names of the large dataset sheets of UK locations."""

"""Enumeration constants container for the columns of the sheets of the large dataset."""
DATE = 0
MEAN_TEMPERATURE = 1
RAINFALL = 2
SUNSHINE = 3
MEAN_WIND_SPEED = 4
MEAN_WIND_SPEED_BC = 5
MAX_GUST = 6
MAX_HUMIDITY = 7
MEAN_CLOUD_COVER = 8
MEAN_VISIBILITY = 9
MEAN_PRESSURE = 10
MEAN_WIND_BEARING = 11
MEAN_WIND_CARDINAL_DIRECTION = 12
MAX_GUST_BEARING = 13
MAX_GUST_CARDINAL_DIRECTION = 14

BEAUFORT_SCALE = ['Calm', 'Light', 'Moderate', 'Fresh']
CARDINAL_DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 
                       'E', 'ESE', 'SE', 'SSE', 
                       'S', 'SSW', 'SW', 'WSW', 
                       'W', 'WNW', 'NW', 'NNW']