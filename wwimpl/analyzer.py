import statistics

class Analyzer:

    #--------------------------------------------------------------------------------
    def __init__(self):
        self.temperature_list_celcius    = []
        self.temperature_list_fahrenheit = []
        self.humidity_list               = []

    #--------------------------------------------------------------------------------
    def set_data(self, weather_data):
        if not isinstance(weather_data, dict):
            raise TypeError("Expecting intput of type DICT but received: " + type(weather_data))

        self.temperature_list_celcius    = []
        self.temperature_list_fahrenheit = []
        self.humidity_list               = []

        try:
          for day_data in weather_data['data']['weather']:
              for hour_data_point in day_data['hourly']:
                self.temperature_list_celcius.append(float(hour_data_point['tempC']))
                self.temperature_list_fahrenheit.append(float(hour_data_point['tempF']))
                self.humidity_list.append(float(hour_data_point['humidity']))
        except Exception as e:
            raise Exception('Could not process provided data:\n' + e)

    #--------------------------------------------------------------------------------
    def temperature_min(self, in_celsius=True):
        if in_celsius:
            return min(self.temperature_list_celcius)
        return min(self.temperature_list_fahrenheit)

    #--------------------------------------------------------------------------------
    def temperature_max(self, in_celsius=True):
        if in_celsius:
            return max(self.temperature_list_celcius)
        return max(self.temperature_list_fahrenheit)

    #--------------------------------------------------------------------------------
    def temperature_average(self, in_celsius=True):
        if in_celsius:
            return statistics.mean(self.temperature_list_celcius)
        return statistics.mean(self.temperature_list_fahrenheit)

    #--------------------------------------------------------------------------------
    def temperature_median(self, in_celsius=True):
        if in_celsius:
            return statistics.median(self.temperature_list_celcius)
        return statistics.median(self.temperature_list_fahrenheit)

    #--------------------------------------------------------------------------------
    def humidity_min(self):
        return min(self.humidity_list)

    #--------------------------------------------------------------------------------
    def humidity_max(self):
        return max(self.humidity_list)

    #--------------------------------------------------------------------------------
    def humidity_average(self):
        return statistics.mean(self.humidity_list)

    #--------------------------------------------------------------------------------
    def humidity_median(self):
        return statistics.median(self.humidity_list)

if __name__ == "__main__":
  raise Exception('World Weather Data Analyzer: Not meant for direct execution.')
