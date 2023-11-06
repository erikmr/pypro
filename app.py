from flask import Flask, Response, make_response, render_template, send_file, stream_with_context,request,jsonify
from datetime import datetime
import requests
import json 
import resend
from flask_cors import CORS,cross_origin


resend.api_key = "re_j7FZ9Rme_4ov44DUobE17FZQEeHR1P46v"

app = Flask(__name__,static_url_path='/static')
CORS(app)
@app.route('/')
def index():  
    hora_actual = datetime.now()
    return render_template("index.html",hora_actual=hora_actual)

@app.route("/confirma_vacuna", methods=['POST'])
@app.route('/confirma_vacuna')
def confirma_vacuna():  
    
    url  = "https://app.vacunainfluenza.com.mx/api/Nf_Data/ExecuteForCRUD"
  
    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    params = request.get_json()

    data = 'ClassName=Vi_Registro_Respuestas_Confirmacion'
    data += '&Action=Get'
    data += '&Registro=' +params["registro"]
    data += '&db=Prometeo_Redes'
    data += '&GetDataModel="false"'
    data += '&GetDataTable="false"'
    print(data)
    res = requests.post(url,data=data, headers=headers)
    response = json.loads(res.text)
    html =  render_template("confirma_vacuna.html",data=response["data"])
    r = resend.Emails.send({
        "from": "soporte@vacunainfluenza.com.mx",
        "to": response["data"][0]["Email"],
        "subject": "Confirmación de registro aplicación vacuna Influenza 2023",
        "html": html
    })
    return r


@app.route("/send_mail", methods=['POST'])
@app.route('/send_mail')
def send_mail():
    hora_actual = datetime.now()
    html =  render_template("confirma_vacuna.html",hora_actual=hora_actual)
    r = resend.Emails.send({
        "from": "soporte@vacunainfluenza.com.mx",
        "to": "emartinez@ensamble.dev",
        "subject": "Prueba",
        "html": html
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