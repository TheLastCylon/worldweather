import json
import requests
from .analyzer import Analyzer

class Retriever:

  #--------------------------------------------------------------------------------
  def __init__(self, api_key):
    self.city          = ''
    self.date_start    = ''
    self.date_end      = ''
    self.api_key       = api_key
    self.data_analyzer = Analyzer()

  #--------------------------------------------------------------------------------
  def request_changed(self, city, date_start, date_end):
    return ((city != self.city ) or (date_start != self.date_start) or (date_end != self.date_end))

  #--------------------------------------------------------------------------------
  def get_analyzer(self, city, date_start, date_end):
    if not self.request_changed(city, date_start, date_end) and self.data_analyzer: # If there was no change, we don't need to hit the worldweatheronline api again.
      return self.data_analyzer
    
    try:
      url      = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={}&q={}&format=json&date={}&enddate={}".format(self.api_key, city, date_start, date_end)
      html_raw = requests.get(url)
      data     = html_raw.json()

      if 'error' in data['data'].keys():
        error_message = data['data']['error'][0]['msg']
        raise Exception("World Weather Online reports:" + error_message)

      self.data_analyzer.set_data(html_raw.json())

      self.city       = city
      self.date_start = date_start
      self.date_end   = date_end

      return self.data_analyzer
    except Exception as e:
      raise Exception('World Weather Data retriever: Could not retrieve data: ' + str(e))

#--------------------------------------------------------------------------------
if __name__ == "__main__":
  raise Exception('World Weather Data retriever: Not meant for direct execution.')
