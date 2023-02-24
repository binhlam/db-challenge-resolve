# -*- encoding: utf-8 -*-
from flask import jsonify, make_response
from pkg.rest.response import response_error, response_success
from pkg.rest.response import CODE_OK, CODE_ERR
from flask_restful import Resource


class GeneratorRequest(Resource):
    def __init__(self, svc):
        self.svc = svc

    def post(self):
        self.svc.logger.info("Starting POST request...")
        res = self.svc.generate()
        if not res:
            err_mess = "Cannot generate xml file!!"
            return make_response(
                jsonify(response_error(err_mess)), CODE_ERR)

        return make_response(
            jsonify(response_success()), CODE_OK)
