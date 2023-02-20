# -*- encoding: utf-8 -*-
CODE_OK = 200
CODE_ERR = 400
CODE_UNAUTHORIZED = 403

ERROR_SCHEMA = {
    'is_success': 0,
    'error_message': 'system error',
}

SUCCESS_SCHEMA = {
    'is_success': 1,
}


def response_error(err=None):
    err_resp = ERROR_SCHEMA.copy()
    if not err:
        return err_resp

    err_resp['error_message'] = err
    return err_resp


def response_success(data=None):
    success_resp = SUCCESS_SCHEMA.copy()
    if data is None:
        return success_resp

    success_resp.update(data)
    return success_resp
