import requests
from random import choice
from flask import request
from app import app
from app.db import Database

# Read API conf
with open('app.conf') as conf:
  api_key = conf.readline().split('=')[1].rstrip('\n')
  api_secret = conf.readline().split('=')[1].rstrip('\n')

base_url = 'http://www.astrobin.com'
api_ver_string = '/api/v1/'
auth_string = 'api_key=' + str(api_key) + '&api_secret=' + str(api_secret) + '&format=json'
iotd_string = 'imageoftheday/?limit=100&offset=1'
iotd_query = base_url + api_ver_string + iotd_string + '&' + auth_string

db = Database()

@app.route('/')
@app.route('/index')
def index():
  return 'Hello, World!'

@app.route('/image', methods=['GET'])
def get_image():
  """Get one of the images of the day"""

  # Check if we need to update the list
  if db.should_update():
    result = requests.get(iotd_query)
    images = []
    for iotd in result.json()['objects']:
      images.append(iotd['image'])
    db.update_list(images)

  # Get one of the images from the database cache
  image = db.get_image()
  if image is None:
    return internal_server_error(None)

  image_query = base_url + str(image) + '?' + auth_string
  result = requests.get(image_query)
  db.log(request.remote_addr, request.user_agent)
  return result.text

@app.errorhandler(404)
def page_not_found(e):
  return 'Error 404', 404

@app.errorhandler(500)
def internal_server_error(e):
  return 'Error 500', 500

