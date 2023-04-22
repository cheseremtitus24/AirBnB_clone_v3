#!/usr/bin/python3
"""
This module Utilizes basic routes and simple
html display and utilizes render_template
which allows rendering of external reference html
files
"""
from flask import Flask, escape, render_template
import os
from models import storage

os.environ["FLASK_APP"] = "7-states_list.py"

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_school():
    """ Function returns a very basic html string without any tags"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def school():
    """ Function returns a very basic html string without any tags"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_func(text):
    """ Function returns a very basic html string and displays parameter
    values and substitutes underscores with an empty space.
    """
    text = text.split('_')
    text = " ".join(text)
    return 'C %s' % escape(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_func(text="is cool"):
    """ Function returns a very basic html string and displays parameter
    values and substitutes underscores with an empty space.
    Also supports default parameter arguments
    """
    text = text.split('_')
    text = " ".join(text)
    return 'Python %s' % escape(text)


@app.route('/number/<int:num>', strict_slashes=False)
def int_display(num):
    """ param num:
                    must be an integer value.
        description:
                    Renders Integer Values only
    """
    return '%d is a number' % num


@app.route('/number_template/<int:num>', strict_slashes=False)
def int_display_template(num):
    """ param num:
                    must be an integer value.
        description:
                    Renders Integer Values on a
                    template file
    """
    return render_template('5-number.html', number=num)


@app.route('/number_odd_or_even/<int:num>', strict_slashes=False)
def int_even_odd_display_template(num):
    """ param num:
                    must be an integer value.
        description:
                    Renders Integer Values and
                    conditionally displays content
                    of the template file
    """
    return render_template('6-number_odd_or_even.html', number=num)

@app.route('/states_list', strict_slashes=False)
def state_list():
    """ Display Listing of all cities:
    """
    states = storage.all('State')

    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
