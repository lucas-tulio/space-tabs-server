import pymysql

# Database access class
class Database:

  def __init__(self):

    self.cur = None
    self.conn = None
    self.is_logging = False

    # Read parameters
    with open('app.conf', 'r') as f:
      f.readline() # Skip the first two rows of the config file
      f.readline()
      self.db_host = f.readline().split('=')[1].rstrip('\n')
      self.db_port = f.readline().split('=')[1].rstrip('\n')
      self.db_user = f.readline().split('=')[1].rstrip('\n')
      self.db_password = f.readline().split('=')[1].rstrip('\n')
      self.db_schema = f.readline().split('=')[1].rstrip('\n')

  def __del__(self):
    self._disconnect()

  def _connect(self):
    self.conn = pymysql.connect(host=self.db_host, port=int(self.db_port), user=self.db_user, passwd=self.db_password, db=self.db_schema, charset='utf8')
    self.cur = self.conn.cursor()

  def _disconnect(self):
    if self.cur != None:
      self.cur.close()
    if self.conn != None:
      self.conn.close()

  def should_update(self):
    """Check if we need to update the list"""

    self._connect()
    try:
      self.cur.execute("""select (created_at) from iotd_updates where created_at > adddate(now(), interval -1 day) order by created_at desc limit 1""")
      results = self.cur.fetchall()
      if len(results) == 0:
        print('Needs to update list')
        self._disconnect()
        return True

    except Exception as e:
      print('Error running query')
      print(e)

    print('List already updated')
    self._disconnect()
    return False

  def update_list(self, images):
    """Update the list of images"""

    self._connect()
    try:
      self.cur.execute("""DELETE FROM iotd_images""")
      for image in images:
        self.cur.execute("""INSERT INTO iotd_images (link) VALUES (%s)""", (image))
      self.cur.execute("""INSERT INTO iotd_updates (created_at) VALUES (now())""")
      self.conn.commit()
      self._disconnect()
      return True
    except Exception as e:
      print('Error running query')
      print(e)

    self._disconnect()
    return False

  def get_image(self):
    """Get one image link from the list"""

    self._connect()
    try:
      self.cur.execute("""select link from iotd_images order by rand() limit 1""")
      row = self.cur.fetchone()
      if row is None:
        print('No images to get')
        self._disconnect()
        return
      image = row[0]
      self._disconnect()
      return image

    except Exception as e:
      print('Error fetching image')
      print(e)

    self._disconnect()
    return None

  def log(self, user_ip, user_agent):
    """Log API access"""

    self._connect()
    try:
      self.cur.execute("""INSERT INTO log (user_ip, user_agent) VALUES (%s, %s)""", (str(user_ip), str(user_agent)))
      self.conn.commit()
      self._disconnect()
      return True
    except Exception as e:
      print('Error saving log')
      print(e)

    self._disconnect()
    return False