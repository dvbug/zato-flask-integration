# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from uuid import uuid4

# Flask
from flask import Flask, render_template

# Flask-WTF
from flask.ext.wtf import Form

# WTForms
from wtforms import SelectField, StringField

app = Flask(__name__)
app.secret_key = uuid4().hex

client_type_choices = (
    ('AnyServiceInvoker', 'AnyServiceInvoker'),
    ('JSONClient', 'JSONClient')
)

class GetCustomerForm(Form):
    cust_id = StringField('cust_id')
    client_type = SelectField('client_type', choices=client_type_choices)

@app.route('/')
def hello():
    template = 'customer.html'
    form = GetCustomerForm()

    form.cust_id.data = '111'

    return render_template(template, form=form)

if __name__ == '__main__':
    app.run(port=8199, debug=True)
