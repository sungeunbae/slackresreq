from flask import Flask, render_template, flash, request, url_for, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, fields
from werkzeug.datastructures import ImmutableMultiDict

import requests
import json
from jinja2 import Template
from datetime import date
import time

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
'usage_details':'Comments'}



with open('templates/request.json',"r") as f:
    msg_template_json = json.load(f)
msg_template = json.dumps(msg_template_json)

#msg_template='{"attachments": [{"fallback": "@brendon.bradley to approve", "color": "#36a64f", "pretext": "@brendon.bradley got a new request", "author_name": "{{form.name}}", "author_link": "form.userlink", "author_icon": "form.userpic", "title": "Core Hours Request", "title_link": "", "text": "-------------------------", "fields": [{"title": "Project Title", "value": "{{form.project_title}}", "short": true}, {"title": "Submitted", "value": "{{form.date}}", "short": true}], "image_url": "", "thumb_url": "", "footer": "QuakeCoRE SW", "footer_icon": "https://wiki.canterbury.ac.nz/download/attachments/49416320/QuakeCore?version=2&modificationDate=1456716670850&api=v2", "ts": "form.ts"}], "parse":"full"}'

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
    usage_details = TextAreaField()

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
        form_dict['ts']=time.time()
            
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
