import os

from flask import Flask, Response

app = Flask(__name__)

SERVICEA_RESPONSE = os.path.join(os.path.dirname(__file__), 'service-a.json')
SERVICEB_RESPONSE = os.path.join(os.path.dirname(__file__), 'service-b.json')
SERVICEC_RESPONSE = os.path.join(os.path.dirname(__file__), 'service-c.json')

@app.route('/servicea/<cpf>')
def servicea(cpf):
    response_data = open(SERVICEA_RESPONSE).read()
    response_data = response_data.replace('XXXXXXXXXXX', cpf)
    return Response(
        response=response_data,
        status=200,
        mimetype='application/json'
    )

@app.route('/serviceb/<cpf>')
def serviceb(cpf):
    response_data = open(SERVICEB_RESPONSE).read()
    response_data = response_data.replace('XXXXXXXXXXX', cpf)
    return Response(
        response=response_data,
        status=200,
        mimetype='application/json'
    )

@app.route('/servicec/<cpf>')
def servicec(cpf):
    response_data = open(SERVICEC_RESPONSE).read()
    response_data = response_data.replace('XXXXXXXXXXX', cpf)
    return Response(
        response=response_data,
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(
        host=os.getenv('SERVER_ADDRESS'),
        port=os.getenv('SERVER_PORT'),
        debug=os.getenv('DEBUG_MODE')
    )