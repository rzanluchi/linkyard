# -*- coding: utf-8 -*-
import falcon
import json

from linkyard import api


class LinkyardResource(object):

    def __init__(self):
        self.api = api.API()

    def on_get(self, req, resp):
        service_name = req.get_param('service_name')
        version = req.get_param('version')
        try:
            result = self.api.get_service(service_name, version)
            resp.status = falcon.HTTP_200
            resp.data = json.dumps({'result': result})
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': str(e)})

    def on_post(self, req, resp):
        data = json.loads(req.stream.read())
        service_name = data.get('service_name', None)
        version = data.get('version', None)
        location = data.get('location', None)
        try:
            self.api.register(service_name, version, location)
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': str(e)})
        else:
            resp.status = falcon.HTTP_201
            resp.body = ''

    def on_put(self, req, resp):
        data = json.loads(req.stream.read())
        service_name = data.get('service_name', None)
        version = data.get('version', None)
        location = data.get('location', None)
        try:
            self.api.health_check(service_name, version, location)
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': str(e)})
        else:
            resp.status = falcon.HTTP_200
            resp.body = ''

    def on_delete(self, req, resp):
        data = json.loads(req.stream.read())
        service_name = data.get('service_name', None)
        version = data.get('version', None)
        location = data.get('location', None)
        try:
            self.api.unregister(service_name, version, location)
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': str(e)})
        else:
            resp.status = falcon.HTTP_200
            resp.body = ''

app = falcon.API()
linkyard = LinkyardResource()
app.add_route('/linkyard', linkyard)
