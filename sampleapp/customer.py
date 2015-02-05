# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from datetime import datetime
from uuid import uuid4

# Flask
from flask import Flask, render_template, request

# Flask-WTF
from flask.ext.wtf import Form

# WTForms
from wtforms import SelectField, StringField

# Zato
from zato.client import AnyServiceInvoker, JSONClient

# ############################################################################

# App

app = Flask(__name__)
app.secret_key = uuid4().hex

# ############################################################################

# Form

client_type_choices = (
    ('AnyServiceInvoker', 'AnyServiceInvoker'),
    ('JSONClient', 'JSONClient')
)

class GetCustomerForm(Form):
    cust_id = StringField('cust_id')
    client_type = SelectField('client_type', choices=client_type_choices)

# ############################################################################

# Zato clients

CLIENT_ADDRESS = 'http://localhost:17010'
CLIENT_PATH_ANY = '/clients/flask/any-service-invoker'
CLIENT_PATH_JSON = '/clients/flask/json-client'
CLIENT_CREDENTIALS = ('flask', 'my-password')

client_any = AnyServiceInvoker(CLIENT_ADDRESS, CLIENT_PATH_ANY, CLIENT_CREDENTIALS)
client_json = JSONClient(CLIENT_ADDRESS, CLIENT_PATH_JSON, CLIENT_CREDENTIALS)

# ############################################################################

@app.route('/')
def hello():
    template = 'customer.html'
    form = GetCustomerForm()

    cust_id = request.args.get('cust_id')

    if cust_id:

        client_type = request.args.get('client_type')

        form.cust_id.data = cust_id
        form.client_type.data = client_type

        # What to invoke the service with
        zato_request = {'cust_id':cust_id}

        # When was the service invoked
        before = datetime.utcnow()

        if client_type == 'AnyServiceInvoker':
            response = client_any.invoke('customer.get1', zato_request)
        else:
            response = client_json.invoke(zato_request)

        # How long we waited for the response, in milliseconds
        time = int((datetime.utcnow() - before).total_seconds() * 1000)

    else:
        response, time = None, None

    return render_template(template, form=form, time=time, response=response)

if __name__ == '__main__':
    app.run(port=8199, debug=True)
