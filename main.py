from flask import Flask, render_template, flash, request, url_for, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, fields
from werkzeug.datastructures import ImmutableMultiDict

import requests
import json
from jinja2 import Template
from datetime import date

# App config.
DEBUG = True
app = Flask(__name__,static_url_path="/static", static_folder="./static")
app.config.from_object(__name__)
app.config.SECRET_KEY = '7d441f27d441f27567d441f2b6176a'

input_field_dict={'name':'SlackID',
'project_title':'Project Title',
'comp_details':'Computational details',
'est_hours':'Estimated',
'req_hours':'Request',
'duration':'Duration',
'justification':'Request Justification',
'last_reqed':'Last Requested',
'last_used':'How much used',
'usage_detail':'Comments'}


msg_template = '{"channel": "BMJGT2NR2", \
    "blocks": [ {"type": "divider"}, \
                {"type": "section", "text": {"type": "mrkdwn", "text": "You have a new request:\n*<https://uceqeng.slack.com/team/{{userid}}|{{form.name}} - HPC allocation request>*"}}, \
                {"type": "section", "fields": [ \
                                        {"type": "mrkdwn", "text": "*Project Title:*\n{{form.project_title}}"}, \
                                        {"type": "mrkdwn", "text": "*When:*\nSubmitted {{form.date}}"} \
                                    ]\
                }, \
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Computational Details:*\n{{form.comp_details}}"}},\
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Estimated/Requested/Duration:*\n{{form.est_hours}} chrs/{{form.req_hours}} chrs/{{form.duration}} weeks"}},\
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Request Justification:*\n{{form.justification}}"}},\
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Last Asked/Used :*\n{{form.last_reqed}} chrs/{{form.last_used}} chrs"}},\
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Comment:*\n{{form.usage_detail}}"}},\
                {"type": "actions", "elements": [ \
                                            {"type": "button", "text": {"type": "plain_text", "emoji": true, "text": "Approve"}, "style": "primary", "value": "click_me_123"}, \
                                            {"type": "button", "text": {"type": "plain_text", "emoji": true, "text": "Deny"}, "style": "danger", "value": "click_me_123"}\
                                    ]\
                },\
                {"type": "divider"}\
    ],\
    "attachments":[\
        {\
            "color":"good"\
        }\
    ],\
    "parse": "full"\
}'

class AttributeDict(dict): 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

class ReusableForm(Form):
    name = TextField()
    project_title = TextAreaField()
    comp_details = TextAreaField()

    est_hours = TextField()
    req_hours = TextField()
    duration = TextField()

    justification = TextAreaField()
    last_reqed = TextField()
    last_used = TextField()
    usage_detail = TextAreaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload_dict = {}
        for key in self._fields:
            self._fields[key].label = fields.core.Label(key,input_field_dict[key])
            self._fields[key].validators.append(validators.InputRequired())
       
        

def text_formatter(form):
    # text=""
    # for key in form:
    #     print(key)
    #     text+="*{}*\n".format(key.upper())
    #     text+=(">"+form[key]+"\n")
    t = Template(msg_template)
    text = t.render(form=form)
    return text

    
@app.route("/", methods=['GET', 'POST'])
def send_to_slack():
    form = ReusableForm(request.form)

    

    #print(form.errors)
    if request.method == 'POST':
             
        url = "https://hooks.slack.com/services/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"
        #form_dict = request.form.to_dict(flat=True)
        form_dict=AttributeDict()
        for key in request.form:
            form_dict[key] = request.form[key]
        form_dict['date']= date.today()
            
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        
   #   print(name)

        if form.validate():
            # Save the comment here.
            
            #return redirect("https://uceqeng.slack.com/messages/CLUE36LQK")
            
            #text=str(msg_template).replace("\'","\"")
            text=text_formatter(form_dict)
            print(text)
        
            r = requests.post(url, data='%s'%text, headers=headers)

            #return redirect("https://uceqeng.slack.com/messages/D1LD6HC56") #sung's DM
#     else:
#        flash('All the form fields are required. ')

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()
