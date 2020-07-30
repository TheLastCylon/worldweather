# worldweather
This is a quick and dirty demonstration of using Python to provide a rest-full API, *without* using a framework of any kind.
It provides weather data such that one can access minimum, maximum, average and median results, of humidity and temperature, for a given city, over a specified period.

# Assumptions
- This requirement is of a hisorical nature. i.e. The user want's to access weather data from an historical perspective, meaning that future weather is not in question.
- This implimentation will be using Python3.x
- This implimentation will be running on a modern Linux system
- The user will not be requesting data for more than 31 days at a time.

# Running the server
You can start the server with the following command, executed on the command line: ```python3 ./worldweather.py```

By default, the server will utilze port *8080* on *localhost*.
This can be changed by passing in a port number on the command line. ```python3 ./worldweather.py 8000```

# The API
The provided API can be broken into two groups: Temperature and Humidity.
## Temperature
### Minimum
Request:```http://localhost:8080/wwapi/temperature/min?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"temperature": {"min": 16.0}}```

### Maximum
Request:```http://localhost:8080/wwapi/temperature/max?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"temperature": {"max": 16.0}}```

### Average
Request:```http://localhost:8080/wwapi/temperature/average?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"temperature": {"average": 21.419354838709676}}```

### Median
Request:```http://localhost:8080/wwapi/temperature/median?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"temperature": {"median": 21.0}}```

### All Temperature data
Request:```http://localhost:8080/wwapi/temperature?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"temperature": {"min": 16.0, "max": 29.0, "median": 21.0, "average": 21.419354838709676}}```

## Humidity
### Minimum
Request:```http://localhost:8080/wwapi/humidity/min?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"humidity": {"min": 36.0}}```

### Maximum
Request:```http://localhost:8080/wwapi/humidity/max?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"humidity": {"max": 90.0}}```

### Average
Request:```http://localhost:8080/wwapi/humidity/average?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"humidity": {"average": 68.58467741935483}}```

### Median
Request:```http://localhost:8080/wwapi/humidity/median?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"humidity": {"median": 70.0}}```

### All Humidity data
Request:```http://localhost:8080/wwapi/humidity?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"humidity": {"min": 36.0, "max": 90.0, "median": 70.0, "average": 68.58467741935483}}```

## Feeling Greedy?
### Get everything
Request:```http://localhost:8080/wwapi/all?city=Cape%20Town&start_date=2020-01-01&end_date=2020-01-31```
Response: ```{"humidity": {"min": 36.0, "max": 90.0, "median": 70.0, "average": 68.58467741935483}, "temperature": {"min": 16.0, "max": 29.0, "median": 21.0, "average": 21.419354838709676}}```

## Dealing with errors
All API errors will be reported as in the example below.

Example: ```{"ERROR": "Date values must be provided in YYYY-MM-DD format!"}```
