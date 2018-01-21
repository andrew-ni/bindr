from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Student, Event
from app import app
import requests
import json

engine = create_engine('sqlite:///events.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index')
def home():
    all_events = session.query(Event).all()
    events_list = []
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

    #coordJSON = jsonify(eventsCoords)
    #return render_template("main.html",events = all_events,coordJSON=coordJSON)
    return render_template("main.html",events = all_events, eventsList = events_list)

@app.route('/host', methods=['GET','POST','BACK'])
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
        return redirect(url_for('home'))
    else:
        print('asdf')
        return render_template("host.html")
    return "asdf"
