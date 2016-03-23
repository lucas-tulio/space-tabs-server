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
      self.cur.execute("""select (created_at) from iotd_updates order by created_at desc limit 1""")
      for row in self.cur.fetchall():
        print(row)

      self._disconnect()
      return True
    except Exception as e:
      print('Error running query')
      print(e)

    self._disconnect()
    return False

  def update_list(self):
    """Update the list of images"""

    self._connect()
    try:
      self.cur.execute()
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
    pass
