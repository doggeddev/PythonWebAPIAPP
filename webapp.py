from flask import Flask, render_template, request
import requests

"""Weather API/APP using Flask.

   Created by Richard Drexel, 02/11/2017

   Purpose is to deliver weather conditons for a location chosen by the user. This information may be obtained by
   calling the GET /weather endpoint, or by navigating to a web page and inputting in the information.

    This program is simply for practice and learning more about APIs, routing, and HTTP Requests/Responses.

"""


app = Flask(__name__)


#API Endpoint 
@app.route('/weather', methods=['GET'])
def apiweather():

    homeJsonObject = None
    workJsonObject = None


    for param in request.args:
        if param == 'home':
            homeJsonObject = check_home_location(request.args['home'])
        if param == 'work':
            workJsonObject = check_work_location(request.args['work'])

    return determine_return_values(homeJsonObject, workJsonObject)


#This receives information from the web page making the request
@app.route('/weather', methods=['POST'])
def weather():

    home = ''
    work = ''

    home = request.form['home']
    home = request.form['home']
    work = request.form['work']

    home_json_object = check_home_location(home)
    work_json_object = check_work_location(work)

    template = determine_return_values(home_json_object, work_json_object)

    return  template


def check_home_location(home):
    homeobject = None

    if home is not '':
        homecoords = home.split(',')

        lat = str.strip(homecoords[0])
        lon = str.strip(homecoords[1])

        rlist0 = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=2350adbb3165e0ae4f996481c837eb8b')
        homeobject = rlist0.json()

    return homeobject


def check_work_location(work):
    workobject = None

    if work is not '':
        workcoords = work.split(',')

        lat = str.strip(workcoords[0])
        lon = str.strip(workcoords[1])



        rlist1 = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=2350adbb3165e0ae4f996481c837eb8b')
        workobject = rlist1.json()

    return workobject

def determine_return_values(home_json_object, work_json_object):

    template = None

    if home_json_object is None and work_json_object is None:
        template = render_template('conditonspage.html', home ='', work ='')
        return template

    if home_json_object == work_json_object:
         template = render_template('conditonspage.html', home=home_json_object, work='')
         return template

    if work_json_object is None:
         template = render_template('conditonspage.html', home=home_json_object, work='')
         return template

    if home_json_object is None:
        template = render_template('conditonspage.html', home='', work=work_json_object)
        return template

    return  render_template('conditonspage.html', home=home_json_object, work=work_json_object)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
