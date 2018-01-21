from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Student
from app import app

engine = create_engine('sqlite:///students.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/index')
def index():
    all_students = session.query(Student).all()
    return render_template("main.html",students = all_students)

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/host')
def host():
    return render_template("main.html")