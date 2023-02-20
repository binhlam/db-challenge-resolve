# -*- encoding: utf-8 -*-
from flask import jsonify, make_response
from app.service.generator import GeneratorService
from pkg.rest.response import response_error, response_success
from pkg.rest.response import CODE_OK, CODE_ERR
from flask_restful import Resource, reqparse
import logging

_logger = logging.getLogger('db-challenge')


class Generatorequest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(Generatorequest, self).__init__()

    def post(self):
        _logger.info("Starting POST request...")
        res = GeneratorService().generate()
        if not res:
            err_mess = "Cannot generate xml file!!"
            return make_response(
                jsonify(response_error(err_mess)), CODE_ERR)

        return make_response(
            jsonify(response_success()), CODE_OK)
