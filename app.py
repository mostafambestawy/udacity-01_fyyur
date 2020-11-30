
#----------------------------------------------------------------------------#
# Refrences
#----------------------------------------------------------------------------#
#https://stackoverflow.com/
#https://www.sqlalchemy.org/
#https://www.mysqltutorial.org/
#https://code.visualstudio.com/docs

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import case ,inspect,func,cast,Date
from datetime import datetime,timedelta
import time

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate=Migrate(app,db)

# TO-done-DO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website= db.Column(db.String(120))
    seeking_talent=db.Column(db.Boolean)
    seeking_description=db.Column(db.String)
    venue_shows=db.relationship('Show' ,backref='venue_shows',  cascade="all,delete",lazy=True)

    def toJson(self):
      return{
        "id":self.id,
        "name":self.name,
        "city":self.city,
        "state":self.state,
        "genres":self.genres,
        "image_link":self.image_link,
        "address":self.address,
        "phone":self.phone,
        "facebook_link":self.facebook_link,
        "venue_shows":self.venue_shows,
      }

    # TO-done-DO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website= db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    artist_shows=db.relationship('Show' ,backref='artist_shows',cascade="all,delete", lazy=True)
    seeking_venue=db.Column(db.Boolean)
    seeking_description=db.Column(db.String)

    def toJson(self):
      return{
        "id":self.id,
        "name":self.name,
        "city":self.city,
        "state":self.state,
        "genres":self.genres,
        "image_link":self.image_link,
        "phone":self.phone,
        "website":self.website,
        "facebook_link":self.facebook_link,
        "seeking_venue":self.seeking_venue,
        "seeking_description":self.seeking_description,
        "artist_shows":self.artist_shows
      }
   
    # TO-done-DO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id=db.Column(db.Integer,db.ForeignKey('Artist.id',ondelete="CASCADE"))
  venue_id=db.Column(db.Integer,db.ForeignKey('Venue.id',ondelete="CASCADE"))
  start_time=db.Column(db.DateTime)



# TO-done-DO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.



#----------------------------------------------------------------------------#
# Create DataBase Tables.
#----------------------------------------------------------------------------#
#db.drop_all()
db.create_all()

#----------------------------------------------------------------------------#
# Helpers
#----------------------------------------------------------------------------#

def listToString(list):
  result=""
  for item in list:
    result=result+item+","
  result=result[:-1]
  return result

#----------------------------------------------------------------------------#
# Insert Data.
#----------------------------------------------------------------------------#

def insertData():
  venues=[{
    "id": 1,
    "name": "1 The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "website": "https://www.themusicalhop.com",
    "seeking_talent": True,
    "seeking_description":"we are seekinkg 2 artists within the coming 2 weeks",
    "phone": "123-444-1234",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "facebook_link": "https://www.facebook.com/TheMusicalHop"
    },
    {
    "id": 2,
    "name": "2 The Dueling Pianos Bar",
    "genres": ["Jazz", "Swing", "Folk"],
    "address": "220 Folsom Swing Street",
    "city": "New York",
    "state": "NY",
    "phone": "123-888-1234",
     "website": "https://www.themusicalhop.com",
    "seeking_talent": False,
    "seeking_description":"",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    },
    {
    "id": 3,
    "name": "3 Park Square Live Music & Coffee",
    "genres": [ "Reggae", "Swing", "Classical"],
    "address": "777 Folsom Coffee Street",
 	  "city": "New York",
    "state": "NY",
    "phone": "123-888-1234",
     "website": "https://www.themusicalhop.com",
    "seeking_talent": True,
    "seeking_description":"we are seekinkg 10 artists within the comong 3 months",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }]
  artists=[{
    "id":1,
    "name": "1 Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "seeking_venue": True,
    "seeking_description":"seeking a venue in San Francisco urgently "
   
    },
    {
    "id":2,
    "name": "2 Matt Quevedo",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
     "seeking_venue": True,
    "seeking_description":"seeking a venue in San Francisco 3000 fans "
   
   },
    {
     "id":3,
    "name": "3 The Wild Sax Band ",
    "genres": ["Rock n Roll"],
    "city": "New York",
    "state": "NY",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
   "seeking_venue": True,
    "seeking_description":"seeking a venue in  New York within one month "
   },
   {
     "id":4,
    "name": "4 Horizons Band",
    "genres": ["Rock n Roll"],
    "city": "New York",
    "state": "NY",
    "phone": "326-999-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "seeking_venue": False,
    "seeking_description":""
    }]
  shows=[
    {
      "id":1,
      "venue_id":1,
      "artist_id":1,
      "start_time":(datetime.today()+timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":2,
      "venue_id":1,
      "artist_id":2,
      "start_time":(datetime.today()-timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":3,
      "venue_id":1,
      "artist_id":3,
      "start_time":(datetime.today()-timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":4,
      "venue_id":2,
      "artist_id":1,
      "start_time":(datetime.today()+timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    },{
      "id":5,
      "venue_id":2,
      "artist_id":2,
      "start_time":(datetime.today()+timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":6,
      "venue_id":2,
      "artist_id":3,
      "start_time":(datetime.today()-timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":7, 
      "venue_id":3,
      "artist_id":1,
      "start_time":(datetime.today()+timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":8,
      "venue_id":3,
      "artist_id":2,
      "start_time":(datetime.today()+timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":9,
      "venue_id":3,
      "artist_id":3,
      "start_time":(datetime.today()+timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    },
     {
      "id":10,
      "venue_id":1,
      "artist_id":4,
      "start_time":(datetime.today()+timedelta(days=17)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":11,
      "venue_id":1,
      "artist_id":4,
      "start_time":(datetime.today()-timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
      "id":12,
      "venue_id":1,
      "artist_id":4,
      "start_time":(datetime.today()-timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    },]
  if len(db.session.query(Venue.id).all())==0:
    for v in venues:
      vn=Venue(
        id=v["id"],
        name=v["name"],
        genres=listToString(v["genres"]),
        city = v["city"],
        state =v["state"],
        address = v["address"],
        phone = v["phone"],
        image_link = v["image_link"],
        facebook_link = v["facebook_link"],
        website=v["website"],
        seeking_talent=v["seeking_talent"],
        seeking_description=v["seeking_description"]
        
      )
      db.session.add(vn)
  if len(db.session.query(Artist.id).all())==0:
    for a in artists:
      ar= Artist(
        id=a["id"],
        name=a["name"],
        genres=listToString(a["genres"]),
        city = a["city"],
        state =a["state"],
        phone = a["phone"],
        image_link = a["image_link"],
        website=a["website"],
        facebook_link = a["facebook_link"],
        seeking_venue=a["seeking_venue"],
        seeking_description=a["seeking_description"]
        
      ) 
      db.session.add(ar)
  if len(db.session.query(Show.id).all())==0:
    for s in shows:
      vn=Show(
        id=s["id"],
        artist_id=s["artist_id"],
        venue_id=s["venue_id"],
        start_time= datetime.strptime(s["start_time"],"%Y-%m-%d %H:%M:%S")
      )
      db.session.add(vn)
  db.session.commit()



  
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  try:
    date = dateutil.parser.parse(value)
  except:
    date=value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

@app.route('/db/populate')
def dbPopulate():
  try:
    insertData()
    return "Done Successfully"
  except Exception as e:
    db.session.rollback()
    return "Failed \nerror:"+e
  finally:
    db.session.close()
    pass
  

#  Venues
#  ----------------------------------------------------------------

  



@app.route('/venues')
def venues():
  # TO-done-DO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  try:
    data=[]
    venues=db.session.query(Venue.city,Venue.state,func.array_agg(Venue.id).label('venues')).group_by(Venue.city,Venue.state).all()
    for venue in venues:
      dataItem={
          'city':venue[0],
          'state':venue[1],
        }
      ids=venue[2]
      vns_ar=[]
      for id in ids:
        venue_id_name=db.session.query(Venue.id,Venue.name).filter(Venue.id==id).first()
        up_shows=db.session.query(func.count(Show.id)).filter(Show.venue_id==id).filter(Show.start_time>datetime.today()).all()
        vns_ar.append({'id':venue_id_name[0],'name':venue_id_name[1],'num_upcoming_shows':up_shows[0],})
      dataItem['venues']=vns_ar
      data.append(dataItem)
  except:
    db.session.rollback()
  finally:
    db.session.close()
#----------------------------------------------------------------------------#
# Data structure.
#----------------------------------------------------------------------------# 
  '''
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  #data=db.session.query(Venue.city,Venue.state,Venue.venue_shows).group_by(Show.venue_id,Venue.id,Venue.state,Venue.city).join(Show).order_by(Venue.venue_shows).all()
  '''
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TO-done-DO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=str(request.form.get('search_term', '')).lower()
  try:
    result=db.session.query(Venue.id,Venue.name).filter((func.lower(Venue.name)).like('%'+search_term+'%')).all()
    data=[]
    for row in result:
      upcoming=db.session.query(func.count(Show.id)).filter(Show.venue_id==int(row[0])).filter(Show.start_time<datetime.today()).first()
      data.append({  "id": row[0],
        "name": row[1],
          "num_upcoming_shows": upcoming[0],
        })
    response={
      'count':len(data),
      'data':data,
    }
  except:
    db.session.rollback()
  finally:
    db.session.close()
#----------------------------------------------------------------------------#
# Data structure.
#----------------------------------------------------------------------------# 
  '''
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  '''
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TO-done-DO: replace with real venue data from the venues table, using venue_id
  try:
    venue_query=db.session.query(
      Venue.id,
      Venue.name,
      Venue.genres,
      Venue.address,
      Venue.city,
      Venue.state,
      Venue.phone,
      Venue.website,
      Venue.facebook_link,
      Venue.seeking_talent,
      Venue.seeking_description,
      Venue.image_link,
    ).filter(Venue.id==venue_id).first()
    data={}
    if venue_query:
      data['id']=venue_query[0]
      data['name']=venue_query[1]
      data['genres']= stringToList(venue_query[2])
      data['address']=venue_query[3]
      data['city']=venue_query[4]
      data['state']=venue_query[5]
      data['phone']=venue_query[6]
      data['website']=venue_query[7]
      data['facebook_link']=venue_query[8]
      data['seeking_talent']=venue_query[9]
      data['seeking_description']=venue_query[10]
      data['image_link']=venue_query[11]
      past_shows=db.session.query(Show.id,Artist.name,Artist.image_link,Show.start_time).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.today()).all()
      ps_array=[]
      for ps in past_shows:
        ps_array.append(
          {
            "artist_id": ps[0],
        "artist_name": ps[1],
        "artist_image_link":ps[2],
        "start_time": ps[3]
          }
        )
      data['past_shows']=ps_array
      data['past_shows_count']=len(ps_array)
      upcoming_shows_count=db.session.query(Show.id,Artist.name,Artist.image_link,Show.start_time).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.today()).all()
      up_array=[]
      for up in upcoming_shows_count:
        up_array.append(
          {
            "artist_id": up[0],
        "artist_name": up[1],
        "artist_image_link":up[2],
        "start_time": up[3]
          }
        )
      data['upcoming_shows']=up_array
      data['upcoming_shows_count']=len(up_array)
    else:
      return render_template('errors/404.html'), 404
  except:
    db.session.rollback()
  finally:
    db.session.close()

    
  '''
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
'''
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = NewVenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TO-done-DO: insert form data as a new Venue record in the db, instead
  # TO-done-DO: modify data to be the data object returned from db insertion
  
  try:
    r_name = request.form.get('name')
    r_city = request.form.get('city')
    r_state = request.form.get('state')
    r_address = request.form.get('address')
    r_phone = request.form.get('phone')
    r_genres = request.form.getlist('genres')
    r_image_link = request.form.get('image_link')
    r_facebook_link = request.form.get('facebook_link')
    r_seeking_talent= request.form.get('seeking_talent')
    r_seeking_description= request.form.get('seeking_description')
    r_website=request.form.get('seeking_description')
    venue= Venue(
    name=r_name,
    city=r_city,
    state=r_state,
    phone=r_phone,
    address=r_address,
    genres=listToString(r_genres),
    image_link=r_image_link,
    facebook_link=r_facebook_link,
    seeking_talent= r_seeking_talent=='y',
    seeking_description=r_seeking_description,
    website=r_website,
    )
    db.session.add(venue)
    db.session.flush()
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' is successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
    return render_template('pages/home.html')
  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TO-done-DO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')




@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TO-done-DO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
    db.session.query(Venue).filter(Venue.id==int(venue_id)).delete()
    db.session.commit()
    flash('Venue is successfully deleted!')
  except Exception as e:
    db.session.rollback()
    flash('Failed to delete venue !')
  finally:
    db.session.close()
    return redirect(url_for('index'))
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  try:
    artists=db.session.query(Artist.id,Artist.name).order_by(Artist.id).all()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # TO-done-DO: replace with real data returned from querying the database
  '''
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  '''
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TO-done-DO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  try:
    search_term=str(request.form.get('search_term', '')).lower()
    artist_query=db.session.query(
      Artist.id,
      Artist.name,
    ).filter((func.lower(Artist.name)).like('%'+search_term+'%')).all()
    data_arr=[]
    data={}
    for artist in artist_query:
      up_shows=db.session.query(func.count(Show.id)).filter(Show.artist_id==int(artist[0])).filter(Show.start_time>datetime.today()).first()
      data_arr.append({
        "id": artist[0],
        "name": artist[1],
        "num_upcoming_shows": up_shows,
      })
    response={
      "count": len(data_arr),
      "data": data_arr
    }
  except:
    db.session.rollback()
  finally:
    db.session.close()
  '''
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  '''
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

def stringToList(text):
  return text.split(",")


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TO-done-DO: replace with real venue data from the venues table, using venue_id
  try:
    data={}
    artistData = Artist.query.filter(Artist.id==artist_id).first()
    data.update(artistData.toJson())
    data.update({"genres":[g for g in (artistData.toJson()["genres"]).split(",")]})
  
    comingShowsQuery=db.session.query(
      Show.venue_id,
      (Venue.name).label('venue_name'),
      (Venue.image_link).label('venue_image_link'),
      Show.start_time,
    ).join(Artist,Show.artist_id==Show.id).join(Venue,Show.venue_id==Venue.id).filter(Artist.id==artist_id).filter(Show.start_time>datetime.today()).all()
    comingShows=[ s for s in comingShowsQuery]
    data.update({"upcoming_shows":comingShows})
    data.update({"upcoming_shows_count":len(comingShows)})

    past_shows=db.session.query(Show.id).join(Artist,Show.artist_id==Show.id).filter(Artist.id==artist_id).filter(Show.start_time<datetime.today()).all()
    
    
    data.update({"past_shows_count": len(past_shows)})
  except:
    db.session.rollback()
  finally:
    db.session.close()
  '''
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  '''
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_query=db.session.query(Artist.id,
  Artist.name,
  Artist.genres,
  Artist.city,
  Artist.state,
  Artist.phone,
  Artist.website,
  Artist.facebook_link,
  Artist.seeking_venue,
  Artist.seeking_description,
  Artist.image_link).filter(Artist.id==int(artist_id)).first()
  if artist_query:
    artist={
    "id": artist_query[0],
    "name": artist_query[1],
    "genres":stringToList(artist_query[2]),
    "city":artist_query[3],
    "state": artist_query[4],
    "phone": artist_query[5],
    "website": artist_query[6],
    "facebook_link": artist_query[7],
    "seeking_venue": artist_query[8],
    "seeking_description":artist_query[9],
    "image_link": artist_query[10]
  }
  form = ArtistForm(obj=artist_query)
  '''
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  '''
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TO-done-DO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  r_name = request.form.get('name')
  r_city = request.form.get('city')
  r_state = request.form.get('state')
  r_phone = request.form.get('phone')
  r_genres = request.form.getlist('genres')
  r_image_link = request.form.get('image_link')
  r_facebook_link = request.form.get('facebook_link')
  r_seeking_venue= request.form.get('seeking_venue')
  r_seeking_description= request.form.get('seeking_description')
  artist= {
      "name":r_name,
      "city":r_city,
      "state":r_state,
      "phone":r_phone,
      "genres":listToString(r_genres),
      "image_link":r_image_link,
      "facebook_link":r_facebook_link,
      "seeking_venue": r_seeking_venue=='y',
      "seeking_description":r_seeking_description,
  }
  db.session.query(Artist).filter(Artist.id==artist_id).update(artist)
  db.session.commit()
  flash('Artist ' + request.form['name'] + ' is successfully listed!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue_query=db.session.query(Venue.id,
  Venue.name,
  Venue.genres,
  Venue.address,
  Venue.city,
  Venue.state,
  Venue.phone,
  Venue.website,
  Venue.facebook_link,
  Venue.seeking_talent,
  Venue.seeking_description,
  Venue.image_link).filter(Venue.id==int(venue_id)).first()
  if venue_query:
    venue={
    "id": venue_query[0],
    "name": venue_query[1],
    "genres":stringToList(venue_query[2]),
    "address":venue_query[3],
    "city":venue_query[4],
    "state": venue_query[5],
    "phone": venue_query[6],
    "website": venue_query[7],
    "facebook_link": venue_query[8],
    "seeking_talent": venue_query[9],
    "seeking_description":venue_query[10],
    "image_link": venue_query[11]
  }
  form = VenueForm(obj=venue_query)
  '''
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  '''
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  r_name = request.form.get('name')
  r_city = request.form.get('city')
  r_state = request.form.get('state')
  r_phone = request.form.get('phone')
  r_genres = request.form.getlist('genres')
  r_address = request.form.get('address')
  r_image_link = request.form.get('image_link')
  r_facebook_link = request.form.get('facebook_link')
  r_seeking_talent= request.form.get('seeking_talen')
  r_seeking_description= request.form.get('seeking_description')
  venue= {
      "name":r_name,
      "city":r_city,
      "state":r_state,
      "phone":r_phone,
      "address":r_address,
      "genres":listToString(r_genres),
      "image_link":r_image_link,
      "facebook_link":r_facebook_link,
      "seeking_talent": r_seeking_talent=='y',
      "seeking_description":r_seeking_description,
  }
  db.session.query(Venue).filter(Venue.id==venue_id).update(venue)
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = NewArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  # called upon submitting the new artist listing form
  # DONE TO-done-DO: insert form data as a new Artist record in the db, instead
  # TO-doneDO: modify data to be the data object returned from db insertion
  try:
    r_name = request.form.get('name')
    r_city = request.form.get('city')
    r_state = request.form.get('state')
    r_phone = request.form.get('phone')
    r_genres = request.form.getlist('genres')
    r_image_link = request.form.get('image_link')
    r_facebook_link = request.form.get('facebook_link')
    r_seeking_venue= request.form.get('seeking_venue')
    r_seeking_description= request.form.get('seeking_description')
    artist= Artist(
      name=r_name,
      city=r_city,
      state=r_state,
      phone=r_phone,
      genres=listToString(r_genres),
      image_link=r_image_link,
      facebook_link=r_facebook_link,
      seeking_venue= r_seeking_venue=='y',
      seeking_description=r_seeking_description,
     
    )
    db.session.add(artist)
    db.session.flush()
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' is successfully listed!')
  except Exception as e:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed')
  finally:
    db.session.close()
    return render_template('pages/home.html')




  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=db.session.query(Show.venue_id,
  (Venue.name).label('venue_name'),
  Show.artist_id,
  (Artist.name).label('artist_name'),
  (Artist.image_link).label('artist_image_link'),
  Show.start_time).join(Venue,Show.venue_id==Venue.id).join(Artist,Show.artist_id==Artist.id).order_by(Show.start_time.desc()).all()
  '''data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]'''
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    artist_id=int(request.form.get('artist_id'))
    venue_id=int(request.form.get('venue_id'))
    start_time=request.form.get('start_time')
    show=Show(
      artist_id=artist_id,
      venue_id=venue_id,
      start_time=start_time
    )
    db.session.add(show)
    db.session.commit()
    flash('Show is successfully listed!')
  except Exception as e:
    flash(err+' An error occurred. Show could not be listed.')
  finally:
    db.session.close()
    return render_template('pages/home.html')

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TO-done-DO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


