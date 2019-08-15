from flask import Flask, json, request, Response, abort

app = Flask(__name__)


@app.route("/pii", methods=['POST'])
def validate():

    output.set_level(True)
    req = request.headers.items()
    output.info('\n'.join('{}: {}'.format(k, v) for k, v in req))
    output.info("Message Body: " + str(request.data))


        resp = Response("{ \"valid\": \"" + str(result.is_valid) + "\"," +
                        "\"errors\":" + json.dumps(errors) + "}")
        resp.headers['Content-Type'] = 'application/json'
        return resp

    abort(400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8013))

