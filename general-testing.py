from flask import Flask, redirect, url_for, request, render_template
import json
import platform
import psutil
import socket
import backend_signature
import logging
import base64

logging.basicConfig(filename='flsklog.log',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')

def flask_logging(req):
    logging.info("----------------------------------------------------------")
    logging.info("Request header : {}".format(dict(req.headers)))
    logging.info("Request Authorization header : {}".format(req.authorization))
    logging.info("Request param : {}".format(req.query_string.decode('utf-8')))
    logging.info("Request body : {}".format(req.get_data().decode('utf-8')))

# allow backend key for --> /apig/simpletest/bkauth
bkend_auth = "Huawei@123"

app = Flask(__name__)


@app.route("/apig/simpletest/test")
def simple_test():
    flask_logging(request)
    return "Success!"

@app.route("/apig/simpletest")
def simpletest():
    flask_logging(request)
    return "Success!"

@app.route("/apig/simpletest/bkauth")
def simpletest_bkauth():
    flask_logging(request)
    if request.headers.get("identifier"):
        idy_hdr_b64_str = request.headers.get("identifier")
        idy_hdr_b64_bytes = idy_hdr_b64_str.encode("utf-8")
        idy_hdr_byte = base64.b64decode(idy_hdr_b64_bytes)
        idy_hdr_str = idy_hdr_byte.decode("utf-8")
        if idy_hdr_str == bkend_auth:
            return "Success. APIG is authenticated."
        else:
            return "Identification failed.", 404
    else:
        return "No identification header.", 404

@app.route("/apig/simpletest/bksigkey")
@backend_signature.requires_apigateway_signature()
def simpletest_bksigkey():
    flask_logging(request)
    return "Success. Backend signature key is ok."

@app.route("/apig/param")
def input_param():
    flask_logging(request)
    try:
        # mandator
        inputName = request.headers.get("User-name")
        # optional
        reqType = request.headers.get("Request-type")
        # constant
        usrType = request.headers.get("User-type")
        # system
        sourceIp = request.headers.get("Source-IP")
        reqId = request.headers.get("Request-ID")

        rsp_dict = {
            "username" : inputName,
            "request type" : reqType,
            "user type (const. param)" : usrType,
            "source IP (sys. param)": sourceIp,
            "api request id (sys. param)": reqId
            }

        # query / params
        param_limit = request.args.get("limit")
        param_emirate = request.args.get("emirate")

        dubai_msg = "Dubai is the most populous city in the United Arab Emirates (UAE)."
        abudhabi_msg = "Abu Dhabi is the capital and second-most populous city (after Dubai) of the United Arab Emirates."
        otherEmi_msg = "The United Arab Emirates is an elective monarchy formed from a federation of seven emirates."

        if param_emirate == "dubai":
            for q in range(int(param_limit)):
                rsp_dict["dubai-{}".format(q)] = "{}. {}".format(q,dubai_msg)
        elif param_emirate == "abudhabi":
            for q in range(int(param_limit)):
                rsp_dict["abudhabi-{}".format(q)] = "{}. {}".format(q,abudhabi_msg)
        else:
            for q in range(int(param_limit)):
                rsp_dict["others-{}".format(q)] = "{}. {}".format(q,otherEmi_msg)

        return json.dumps(rsp_dict)
    except:
        return "error! chech whether header and params are configured properly in the request.", 404



@app.route("/apig/selflab")
@backend_signature.requires_apigateway_signature()
def selflab():
    flask_logging(request)
    try:
        # mandator
        inputName = request.headers.get("username")
        # optional
        reqType = request.headers.get("Request-Type")
        # constant
        usrType = request.headers.get("User-type")
        # system
        sourceIp = request.headers.get("source-IP")
        reqId = request.headers.get("request-ID")

        rsp_dict = {
            "username" : inputName,
            "request type" : reqType,
            "user type (const. param)" : usrType,
            "source IP (sys. param)": sourceIp,
            "api request id (sys. param)": reqId
            }

        # query / params
        param_limit = request.args.get("limit")
        param_emirate = request.args.get("emirate")

        dubai_msg = "Dubai is the most populous city in the United Arab Emirates (UAE)."
        abudhabi_msg = "Abu Dhabi is the capital and second-most populous city (after Dubai) of the United Arab Emirates."
        otherEmi_msg = "The United Arab Emirates is an elective monarchy formed from a federation of seven emirates."

        if param_emirate == "dubai":
            for q in range(int(param_limit)):
                rsp_dict["dubai-{}".format(q)] = "{}. {}".format(q,dubai_msg)
        elif param_emirate == "abudhabi":
            for q in range(int(param_limit)):
                rsp_dict["abudhabi-{}".format(q)] = "{}. {}".format(q,abudhabi_msg)
        else:
            for q in range(int(param_limit)):
                rsp_dict["others-{}".format(q)] = "{}. {}".format(q,otherEmi_msg)

        return json.dumps(rsp_dict)
    except:
        return "error! Check and try again.", 404






@app.route("/")
def index():
    return "Welcome to test app!"

@app.route("/svrinfo/test")
def svrtest():
    return "success {}".format(request.headers.get("usertype"))

@app.route("/svrinfo")
def svrinfo():
    svrinfo_dict = {
        "Hostname": platform.node(),
        "Machine Type": platform.architecture()[0],
        "Platform Type": platform.platform(),
        "Processor Type": platform.processor(),
        "Logical Cores": psutil.cpu_count(logical=True),
        "Current - CPU Frequency (MHz)": psutil.cpu_freq().current,
        "Max - CPU Frequency (MHz)": psutil.cpu_freq().max,
        "Min - CPU Frequency (MHz)": psutil.cpu_freq().min,
        "CPU Usage (%)": psutil.cpu_percent(interval=1),
        "Per CPU usage (%)": psutil.cpu_percent(interval=1, percpu=True),
        "Total RAM (GB)": round(psutil.virtual_memory().total/1000000000,2),
        "Available RAM (GB)": round(psutil.virtual_memory().available/1000000000,2),
        "Used RAM (GB)": round(psutil.virtual_memory().used/1000000000,2),
        "RAM Usage (%)": psutil.virtual_memory().percent
    }
    svrinfo_json = json.dumps(svrinfo_dict)
    return svrinfo_json

@app.route("/obstest")
def obstest():
    obsurl="https://demo-bucket-p84244532.obs.ae-ad-1.g42cloud.com/castle-01.jpg"
    return render_template("obs.html",objurl=obsurl)



@app.route("/stage")
@backend_signature.requires_apigateway_signature()
def staging():
    username = request.headers.get("username")
    age = request.args.get("age")
    print(request.headers)
    # print(request.get_json())
    print(request.authorization)
    print(request.query_string.decode('utf-8'))
    return "weclome to staging | user : {} age : {}".format(username,age)

@app.route("/release")
def release():
    return "weclome to release"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
