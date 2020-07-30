#!/usr/bin/python3
import os.path
import sys
import json
import datetime
from urllib.parse import urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from wwimpl import retriever, analyzer

#--------------------------------------------------------------------------------
class WorldWeatherHTTPRequestHandler(BaseHTTPRequestHandler):

#--------------------------------------------------------------------------------
  root_page_data    = 'rootpage'
  parsed_url        = None
  data_retriever    = retriever.Retriever('7856d02822474b99b99155147202807')
  data_analyzer     = analyzer.Analyzer()
  api_routing_table = [ '/wwapi/temperature/min',
                        '/wwapi/temperature/max',
                        '/wwapi/temperature/average',
                        '/wwapi/temperature/median',
                        '/wwapi/humidity/min',
                        '/wwapi/humidity/max',
                        '/wwapi/humidity/average',
                        '/wwapi/humidity/median',
                        '/wwapi/temperature',
                        '/wwapi/humidity',
                        '/wwapi/all' ]
    
  #--------------------------------------------------------------------------------
  def do_GET(self):
    try:
      self.parsed_url = urlparse(self.path)

      self.send_response(200)

      if self.parsed_url.path in self.api_routing_table:
          self.send_header('Content-Type', 'application/json')
          self.end_headers()

          try:
            self.do_api_call()
          except Exception as e:
            self.write_json_error(str(e))

      else:
        self.end_headers()
        self.show_root_page()

    except Exception as e:
      error_message = "Could not process request: \n" + str(e)
      self.wfile.write(bytearray(error_message, 'utf-8'))


  #--------------------------------------------------------------------------------
  def build_query_dictionary(self, query_string):
    if len(query_string) <= 0:
      return {}

    query_list       = query_string.split("&")
    query_parameters = {}

    for name_value_pair in query_list:
      nvp_as_list =  name_value_pair.split("=")

      if len(nvp_as_list) != 2:
        raise Exception('Ignoring request with bad URL portion: ' + str(name_value_pair))

      query_parameters[nvp_as_list[0].lower()] = nvp_as_list[1]

    return query_parameters

  #--------------------------------------------------------------------------------
  def show_root_page(self):
    if self.root_page_data == 'rootpage':
      if os.path.isfile('./root_page.html'):
        with open('./root_page.html', mode='r') as rootpage:
          self.root_page_data = rootpage.read()
      else:
        self.root_page_data = "Welcome to the World Weather app ... Sadly, the cool interface file I made seems to be missing. :("

    self.wfile.write(bytearray(self.root_page_data, 'utf-8'))

  #--------------------------------------------------------------------------------
  def do_api_call(self):
    try:
      request_variables       = self.build_query_dictionary(self.parsed_url.query)
      supplied_url_parameters = request_variables.keys()
      city                    = self.validate_city (request_variables)
      dates                   = self.validate_dates(request_variables)
      self.data_analyzer      = self.data_retriever.get_analyzer(city, dates[0], dates[1])
      data2show               = self.get_statistical_result(self.parsed_url.path)

      self.wfile.write(bytearray(json.dumps(data2show), 'utf-8'))
    except Exception as e:
      self.write_json_error(str(e))

  #--------------------------------------------------------------------------------
  def write_json_error(self, message):
    error_dict =  { "ERROR" : message }
    self.wfile.write(bytearray(json.dumps(error_dict), 'utf-8'))

  #--------------------------------------------------------------------------------
  def validate_city(self, request_variables):
    if 'city' not in request_variables.keys():
      raise Exception('City parameter missing from request!')

    if len(request_variables['city']) <= 0:
      raise Exception('Invalid City parameter provided!')

    return request_variables['city']

  #--------------------------------------------------------------------------------
  def validate_dates(self, request_variables):
    max_date_delta = datetime.timedelta(days=31) # We provide for a maximum of 31 days worth of data for now.
    return_dates   = []
    start_date     = None
    end_date       = None

    if 'start_date' not in request_variables.keys():
      raise ValueError('No start date provided!')

    if 'end_date' not in request_variables.keys():
      raise ValueError('No end date provided!')

    try:
      start_date = datetime.datetime.strptime(request_variables['start_date'], '%Y-%m-%d')
      end_date   = datetime.datetime.strptime(request_variables['end_date'  ], '%Y-%m-%d')
    except ValueError:
      raise ValueError("Date values must be provided in YYYY-MM-DD format!")

    if (end_date - start_date) > max_date_delta:
      raise ValueError("Provided dates may not be more than 31 days appart!")

    return_dates.append(str(start_date))
    return_dates.append(str(end_date))
    return return_dates

  #--------------------------------------------------------------------------------
  def get_statistical_result(self, path):
    if path == '/wwapi/temperature/min'    : return { 'temperature' : { 'min'    : self.data_analyzer.temperature_min    () } }
    if path == '/wwapi/temperature/max'    : return { 'temperature' : { 'max'    : self.data_analyzer.temperature_max    () } }
    if path == '/wwapi/temperature/average': return { 'temperature' : { 'average': self.data_analyzer.temperature_average() } }
    if path == '/wwapi/temperature/median' : return { 'temperature' : { 'median' : self.data_analyzer.temperature_median () } }
    if path == '/wwapi/humidity/min'       : return { 'humidity'    : { 'min'    : self.data_analyzer.humidity_min       () } }
    if path == '/wwapi/humidity/max'       : return { 'humidity'    : { 'max'    : self.data_analyzer.humidity_max       () } }
    if path == '/wwapi/humidity/average'   : return { 'humidity'    : { 'average': self.data_analyzer.humidity_average   () } }
    if path == '/wwapi/humidity/median'    : return { 'humidity'    : { 'median' : self.data_analyzer.humidity_median    () } }

    if path == '/wwapi/temperature':
      return {
        'temperature' : {
        'min'    : self.data_analyzer.temperature_min(),
        'max'    : self.data_analyzer.temperature_max(),
        'average': self.data_analyzer.temperature_average(),
        'median' : self.data_analyzer.temperature_median () } }

    if path == '/wwapi/humidity':
      return {
        'humidity': {
          'min'    : self.data_analyzer.humidity_min(),
          'max'    : self.data_analyzer.humidity_max(),
          'average': self.data_analyzer.humidity_average(),
          'median' : self.data_analyzer.humidity_median() } }

    if path == '/wwapi/all':
      return {
        'temperature' : {
          'min'    : self.data_analyzer.temperature_min(),
          'max'    : self.data_analyzer.temperature_max(),
          'average': self.data_analyzer.temperature_average(),
          'median' : self.data_analyzer.temperature_median () },
        'humidity': {
          'min'    : self.data_analyzer.humidity_min(),
          'max'    : self.data_analyzer.humidity_max(),
          'average': self.data_analyzer.humidity_average(),
          'median' : self.data_analyzer.humidity_median() } }


#--------------------------------------------------------------------------------
def main():
  try:
    server_port = 8080

    if len(sys.argv) >= 2:
      server_port = int(sys.argv[1])
      
    print('-- World Weather HTTP Server Start --\n')
    print('Using port: ' + str(server_port))

    httpd = HTTPServer(('localhost', server_port), WorldWeatherHTTPRequestHandler)
    httpd.serve_forever()
  except KeyboardInterrupt:
    print('\nGoodbye! :)')
  except Exception as e:      
    print('\n!!!UNEXPECTED SERVER HALT!!\n' + str(e))


if __name__ == "__main__":
  main()
