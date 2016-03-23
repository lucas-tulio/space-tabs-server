import requests
from random import choice
from app import app

# Read API conf
with open('app.conf') as conf:
  api_key = conf.readline().split('=')[1].rstrip('\n')
  api_secret = conf.readline().split('=')[1].rstrip('\n')

base_url = 'http://www.astrobin.com'
api_ver_string = '/api/v1/'
auth_string = 'api_key=' + str(api_key) + '&api_secret=' + str(api_secret) + '&format=json'
iotd_string = 'imageoftheday/?limit=30&offset=1'
iotd_query = base_url + api_ver_string + iotd_string + '&' + auth_string

@app.route('/')
@app.route('/index')
def index():
  return 'Hello, World!'

@app.route('/image', methods=['GET'])
def get_image():
  '''Get one of the images of the day'''

  # Get the list of iotd
  result = requests.get(iotd_query)
  images = []
  for iotd in result.json()['objects']:
    images.append(iotd['image'])

  # Get one of the images
  image_query = base_url + str(choice(images)) + '?' + auth_string
  result = requests.get(image_query)
  return result.text

@app.errorhandler(404)
def page_not_found(e):
  return 'Error 404', 404

@app.errorhandler(500)
def internal_server_error(e):
  return 'Error 500', 500

