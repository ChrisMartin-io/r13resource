from flask import Flask, render_template, redirect, request, jsonify, \
    url_for, json
from models import GitRepo, GitUser, Lecture, Exercise, db, connect_db
from data import *
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///r13'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def show_index():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    return render_template('index.html',
                           lectures=lectures,
                           exercises=exercises)


@app.route('/add-user')
def show_add_repo():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    return render_template('add-repo.html',
                           lectures=lectures,
                           exercises=exercises)


@app.route('/submit-user', methods=['POST'])
def add_git_user():

    ## Check if user exists on Git
    username = request.form['git_username']
    git_data = requests.get(f'https://api.github.com/users/{username}/repos')

    ## Response if user not found
    if git_data.status_code == 404:
        return render_template('cohort-code.html', message="user not found")

    ## Response if user valid
    elif git_data.status_code == 200:
        content = git_data.content
        parsed_json = json.loads(content)

        ## Call function to parse data
        parse_data(parsed_json)

        return render_template('cohort-code.html',
                               message="user added successfully",
                               gitusers=GitUser.query.all(),
                               gitrepos=GitRepo.query.all())

    ## Response if neither
    else:
        return render_template('cohort-code.html', message="unable to process")

    url = f'https://api.github.com/users/{username}/repos'
    new_user = GitUser(name=username, url=url)

    db.session.add(new_user)
    db.session.commit()

    users = GitUser.query.all()

    return redirect('/cohort-code')


@app.route('/cohort-code')
def cohort_code():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    gitusers = GitUser.query.all()
    gitrepos = GitRepo.query.all()

    return render_template('cohort-code.html',
                           lectures=lectures,
                           exercises=exercises,
                           gitusers=gitusers,
                           gitrepos=gitrepos)


@app.route('/lectures')
def show_lecture():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    lecture_id = int(request.args['id'])

    lecture_url = Lecture.query.get(lecture_id).url

    return render_template('lecture.html',
                           lectures=lectures,
                           exercises=exercises,
                           url=lecture_url)


# @app.route('/lecture/<lecture_id>')
# def show_lecture(lecture_id):
#     lectures = Lecture.query.order_by(Lecture.title)
#     # lecture_url = Lecture.query.filter(Lecture.id == lecture_id)

#     return render_template('new.html')

# Pull current lectures

# @app.route('/lecture')
# def reveal_lecture():
#     soup = get_lectures()
#     links = []
#     titles = []

#     for link in soup.find_all('a'):
#         links.append('http://curric.rithmschool.com/r13/lectures/' +
#                      link.get('href'))

#     for link in links:
#         if 'zip' in link:
#             continue
#         response = requests.get(link)
#         soup = BeautifulSoup(response.text)
#         if (soup.title is None):
#             continue
#         else:
#             titles.append(soup.title.string)

#     lectures = Lecture.query.order_by(Lecture.title)
#     return render_template('new.html',
#                            titles=titles,
#                            links=links,
#                            lectures=lectures,
#                            exercises=exercises)

# @app.route('/lectures')
# def lecture_page():

#     url = 'http://curric.rithmschool.com/r13/lectures/ajax/'
#     return render_template('lecture.html',
#                            url=url,
#                            exercises=exercises,
#                            lectures=lectures)
