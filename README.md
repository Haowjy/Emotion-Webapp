# Set Up Development Environment

## Clone this repository:

    git clone https://github.com/haowjy/UPDATE THIS LATER

## Create a virtualenv and activate it:

    python3 -m venv venv
    source venv/bin/activate

## Install dependencies

    (python -m) pip install -r requirements.txt

## Set up Environments variables

    export FLASK_APP=emotionapp.py
or

    export FLASK_APP=app.py

## Run the app

    flask run

## Update python imports

    (python -m) pip freeze > requirements.txt

# Flask Tutorial
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world