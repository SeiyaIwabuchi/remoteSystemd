from flask import Flask, render_template,request
import os
import re
import numpy as np
app = Flask(__name__)

def getServiceList():
    os.system("systemctl list-unit-files --type=service > servicelist")
    with open("servicelist","r") as f:
        servicelist = f.readlines()
    servicelist = servicelist[1:-2]
    servicelist = list( map(lambda x : x.replace("\n","") ,servicelist) )
    servicelist = list( map(lambda x : re.split("\s+",x)[:2] ,servicelist) )
    servicelist = list(np.array(servicelist).T)
    return servicelist

@app.route('/')
def index():
    return render_template('index.html',service_names=getServiceList()[0])

@app.route("/operation")
def operation():
    serviceName = request.args.get("service_name")
    ope = request.args.get("operation")
    os.system("systemctl {} {} > operes".format(ope,serviceName))
    if ope != "status":
        os.system("systemctl status {} >> operes".format(serviceName))
    with open("operes","r") as f:
        operationResult = f.read().split("\n")
    return render_template(
            "index.html",
            operationResult=operationResult,
            service_names=getServiceList()[0],
            selected=serviceName
        )
## おまじない
if __name__ == "__main__":
    app.run(host="0.0.0.0")