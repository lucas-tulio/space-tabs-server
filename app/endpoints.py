from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Hello, World!'

@app.route('/images', methods=['GET'])
def get_images():
    return 'HUE'

@app.errorhandler(404)
def page_not_found(e):
  return 'Error 404', 404

@app.errorhandler(500)
def internal_server_error(e):
  return 'Error 500', 500

