from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Student, Event
from app import app
from datetime import *
import requests
import json

engine = create_engine('sqlite:///events.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def calcTotalDate(event):
    year = int(event.date[:4])
    month = int(event.date[5:7])
    day = int(event.date[8:])
    hour = int(event.end[:2])
    minute = int(event.end[3:])
    return minute + 60*hour + 60*24*day + 60*24*30*month + 60*24*30*12*year

def calcTotalDateToday():
    now = datetime.now()
    return now.minute + 60*now.hour + 60*24*now.day + 60*24*30*now.month + 60*24*30*12*now.year

def hasPassed(event):
    present = datetime.now()
    year = int(event.date[:4])
    month = int(event.date[5:7])
    day = int(event.date[8:])
    hour = int(event.end[:2])
    minute = int(event.end[3:])
    date = datetime(year, month, day)
    if (date < present):
        return True
    else:
        return 60*hour+minute < 60*present.hour+present.minute

def startIsAfterEnd(event):
    return (60*int(event.start[:2]) + int(event.start[3:])) > (60*int(event.end[:2]) + int(event.end[3:]))

eList = session.query(Event).all()
for event in eList:
    if (hasPassed(event) or startIsAfterEnd(event)):
        session.delete(event)
session.commit()

# sortedEvents = session.query(Event).all()
# sorted(sortedEvents, key=lambda event:(event.date, event.end))

@app.route('/')
@app.route('/index')
def home():
    all_events = session.query(Event).all()
    events_list = []
    for event in all_events:
        if (hasPassed(event) or startIsAfterEnd(event)):
            session.delete(event)
    session.commit()

    for event in all_events:
        events_list.append(
            {
                'id':event.id,
                'name':event.name,
                'loc_name':event.loc_name,
                'lat':str(event.loc_lat),
                'long':str(event.loc_long),
                'subject':event.subject,
                'date':event.date,
                'start':event.start,
                'end':event.end,
                'desc':event.desc
            })

    return render_template("main.html",events = all_events, eventsList = events_list)

@app.route('/host', methods=['GET','POST'])
def host():
    if request.method == 'POST':
        print(request.form['timeEndIn'])
        n = request.form['nameIn']
        loc = request.form['locIn']
        subj = request.form['subjectIn']
        date = request.form['dateIn']
        start = request.form['timeStartIn']
        end = request.form['timeEndIn']
        desc = request.form['descIn']
        #event = Event(name=n,loc_name=loc,subject=subj,date=date,start=start,end=end,desc=desc)

        #using loc get coordinates
        #first separate loc with + to obtain address
        #https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
        address = loc.replace(' ','+')
        result =  json.loads(requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key=AIzaSyAPIKI9rNnmIyT-5frqg6aSqaAS3hUA69k').content.decode('utf-8'))
        #print(result["results"][0].geometry.location.lat)
        lat = result["results"][0]["geometry"]["location"]["lat"]
        lng = result["results"][0]["geometry"]["location"]["lng"]
        event = Event(name=n,loc_name=loc,loc_lat=lat,loc_long=lng,subject=subj,date=date,start=start,end=end,desc=desc)

        session.add(event)
        session.commit()

        # sortedEvents.append(event)
        # sorted(sortedEvents, key=lambda event:(event.date, event.end))

        return redirect(url_for('home'))
    else:
        print('asdf')
        return render_template("host.html")
    return "asdf"
