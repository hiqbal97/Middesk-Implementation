from random import choices
import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import json
from middesk_api import createBusiness, getBusinesses
import pandas

app = Flask(__name__)

app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
Bootstrap(app)

class Business(FlaskForm):
    name = StringField('What is the name of the business?', validators=[DataRequired()])
    address1 = StringField('Address Line 1', validators=[DataRequired()])
    address2 = StringField('Address Line 2')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('Zip Code', validators=[DataRequired()])
    website = StringField('Do you have a website, if so what is it?')
    tin = StringField('Do you have a Tax Identification Number, if so what is it?')
    submit = SubmitField('Submit Information')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = Business()
    if form.validate_on_submit():
        global name
        name = form.name.data
        global address1
        address1 = form.address1.data
        global address2
        address2 = form.address2.data
        global city
        city = form.city.data
        global state
        state = form.state.data
        global zip
        zip = form.zip.data
        global website
        website = form.website.data
        global tin
        tin = form.tin.data
        return redirect(url_for('response'))
    return render_template('create.html', form=form)

@app.route('/response')
def response():
    result = createBusiness(name, address1, address2, city, state, zip, website, tin)
    return render_template('response.html', result=result)

@app.route('/businesses', methods=("POST", "GET"))
def businesses():
    result = getBusinesses()
    return render_template('businesses.html',  tables=[result.to_html(classes='data')], titles=result.columns.values)

if __name__ == '__main__':
    app.run(port=8080, debug=True)