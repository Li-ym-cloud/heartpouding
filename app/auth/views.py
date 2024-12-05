from flask import render_template
from . import auth
from .forms import LoginForm


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = LoginForm()
    return render_template('registration.html', form=form)
