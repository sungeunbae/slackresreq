from flask import Flask, render_template, flash, request, url_for, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.datastructures import ImmutableMultiDict

import requests

# App config.
DEBUG = True
app = Flask(__name__,static_url_path="/static", static_folder="./static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
  name = TextField('SlackID:', validators=[validators.InputRequired()])
  project_title = TextAreaField("Project Title",[validators.InputRequired()])
  comp_details = TextAreaField("Computational details",validators=[validators.InputRequired()])
  
  est_hours = TextField("Estimated",validators=[validators.InputRequired()])
  req_hours = TextField("Request",validators=[validators.InputRequired()])
  duration = TextField("Duration",validators=[validators.InputRequired()])

  justification = TextAreaField("Request Justification",validators=[validators.InputRequired()])
  last_reqed = TextField("Last Requested")
  last_used = TextField("How much used")
  usage_detail = TextAreaField("Comments: ")

def text_formatter(form):
    text=""
    for key in form:
        print(key)
        text+="*{}*\n".format(key.upper())
        text+=(">"+form[key]+"\n")
    return text

    
@app.route("/", methods=['GET', 'POST'])
def send_to_slack():
    form = ReusableForm(request.form)

    #print(form.errors)
    if request.method == 'POST':
             
        url = "https://hooks.slack.com/services/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"
        payload_dict = request.form.to_dict(flat=True)
        # payload_dict={}
        # for key in request.form:
        #     payload_dict[request.form[key].label] = request.form[key]
            
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        


   #   print(name)

        if form.validate():
            # Save the comment here.
            
            #return redirect("https://uceqeng.slack.com/messages/CLUE36LQK")
            
            
            payload_text = text_formatter(payload_dict)    
              
            r = requests.post(url, data='{"text":"%s"}'%payload_text, headers=headers)

            #return redirect("https://uceqeng.slack.com/messages/D1LD6HC56") #sung's DM
#     else:
#        flash('All the form fields are required. ')

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()
