# space-tabs-server
Flask app that consumes Astrobin and NASA APOD API, then serves its images to the Space Tabs extension

### Setup

1. `pip3 install -r requirements.txt`
2. `cp app.conf.dist app.conf` and include database and API info in `app.conf`
3. Run `db/create-schema.sql` in your MySQL database
4. `./run.py`
