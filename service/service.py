# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import logging
import os
import json
import requests
from base64 import b64encode

from werkzeug.exceptions import BadRequest

app = Flask(__name__)

logger = logging.getLogger('document-get-transform')

url_property = os.environ.get("URL_PROPERTY", "gdpr-document:extract-content")
return_property = os.environ.get("RETURN_PROPERTY", "gdpr-document:content")

try:
    connect_timeout = int(os.environ.get("CONNECT_TIMEOUT", "60"))
except ValueError:
    connect_timeout = 60

try:
    read_timeout = int(os.environ.get("READ_TIMEOUT", "3600"))
except ValueError:
    read_timeout = 60


def get_and_encode_data(url):
    r = requests.get(url, timeout=(connect_timeout, read_timeout))
    r.raise_for_status()

    return b64encode(r.content)


@app.route('/get-document', methods=["POST"])
def search():
    entities = request.get_json()

    app.logger.info("Got entities: %s" % repr(entities))

    if not isinstance(entities, list):
        return BadRequest("Payload must be JSON array of entities")

    def perform_get_docs():
        yield b"["

        for ix, entity in enumerate(entities):
            if ix > 0:
                yield b", "

            url = entity.get(url_property)
            if url is not None:
                # GET file and base64 encode it

                logger.info("GET'ing URL '%s'.." % url)
                try:
                    document_data = get_and_encode_data(url)
                    app.logger.info("Got URL '%s'" % url)
                    app.logger.info("document_data: %s" % str(document_data))
                except BaseException as e:
                    logger.exception("Failed to get URL '%s'!" % url)
                    raise e

                if document_data is not None:
                    entity[return_property] = "~b" + str(document_data, encoding="utf-8")
            else:
                app.logger.info("Skipping entity with id '%s' - missing '%s' property!" % (entity["_id"], url_property))

            yield json.dumps(entity)
        yield b"]"

    try:
        return Response(response=perform_get_docs(), status=200, mimetype='application/json')
    except BaseException as e:
        raise BadRequest(description="Failed to download document(s):\n%s" % repr(e))


if __name__ == '__main__':
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))

    app.logger.addHandler(stdout_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.propagate = False

    app.logger.info("What?")

    app.run(debug=False, host='0.0.0.0', port=os.environ.get('PORT', 5000))
