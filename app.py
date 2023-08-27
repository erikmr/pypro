from flask import Flask, Response, make_response, render_template, send_file, stream_with_context,request,jsonify
from datetime import datetime
import requests
import json 
import resend

resend.api_key = "re_gTA3ZJ2C_Gh7PpuMSGxqDHFNhCBFkAAwd"

app = Flask(__name__)

@app.route('/')
def index():  
    return render_template("index.html",num_posts=2)

@app.route('/send_mail')
def send_mail():
    r = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "sistemas@grupokc.com.mx",
        "subject": "Prueba",
        "html": "<p><a href='https://www.grupokc.com.mx'>vinculo</a>Congrats on sending your <strong>first email</strong>!</p>"
    })
    print(r)
    return r


@app.route("/resend_webhook", methods=['POST'])
def resend_webhook():
    print(request.get_json())
    return {}


@app.route("/version", methods=['POST'])
def version():
    # url  = "https://kc-frontback.azurewebsites.net/api/version"
    # res = requests.post(url)
    # response = json.loads(res.text)
    # print(res.text)
    return {
        "version":'1.0.0',
        "project":"pypro"
    }

@app.route("/exe4crud", methods=['POST'])
def exe4crud():
    args= ''    
    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    url  = "https://prometeo.grupokc.com.mx:3002/api/Nf_Data/ExecuteForCRUD"

    print(request.content_type)
    if(request.content_type == 'application/json'):
        args = request.get_json()

        
    if(request.content_type == 'application/x-www-form-urlencoded'):
        args = request.form.to_dict(flat=False)

    args["GetDataModel"] = "false"
    args["GetDataTable"] = "false"
    print(args)

   

    res = requests.post(url,data= args, headers=headers)
    response = json.loads(res.text)
    return response