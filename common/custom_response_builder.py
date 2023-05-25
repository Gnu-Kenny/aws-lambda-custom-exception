import json

from botocore.args import logger

from common.CommonResultCode import CommonResultCode
from common.CustomException import CustomException


def build_success_response(response_data: dict) -> dict:
    """ Response Format
    {
        'headers': {
            'Content-Type': 'application/json'
        },
        "statusCode": 200,
        "body": {
            'code': 'SUCCESS',
            'message': 'success',
            'data': response_data
        },
        "isBase64Encoded": False
    }
    """
    try:
        response: dict = _init_json_response()

        response["statusCode"] = CommonResultCode.SUCCESS.status_code

        response_body = {
            'code': CommonResultCode.SUCCESS.status_code_string,
            'message': CommonResultCode.SUCCESS.message,
            'data': response_data
        }

        response["body"] = json.dumps(response_body, ensure_ascii=False, default=int)

    except Exception as exc:
        logger.exception(exc)
        return _get_response_for_fail_in_building_response("build_success_response")

    return response


def build_fail_response(err) -> dict:
    try:
        response = _init_json_response()

        if isinstance(err, CustomException):
            result_code = err.result_code

            response_body = {
                "code": result_code.status_code_string,
                "message": err.msg if err.msg is not None else result_code.message,
                "data": None
            }
        else:  # UNHANDLED_ERROR
            result_code = CommonResultCode.UNEXPECTED_ERROR
            response_body = {
                "code": result_code.status_code_string,
                "message": result_code.message,
                "data": None
            }

        response["body"] = json.dumps(response_body, ensure_ascii=False)
        response["statusCode"] = result_code.status_code
    except Exception as exc:
        logger.exception(exc)
        return _get_response_for_fail_in_building_response("build_fail_response")

    logger.exception(err)
    return response


def _init_json_response() -> dict:
    response = {
        'headers': {
            'Content-Type': 'application/json'
        },
        "statusCode": None,
        "body": str(None),
        "isBase64Encoded": False
    }

    return response


def _get_response_for_fail_in_building_response(caller_name):
    return {
        "statusCode": 500,
        "headers": {
            'Content-Type': "application/json",
            "req-id": "aws_request_id"
        },
        "body": json.dumps({
            'code': CommonResultCode.BUILD_RESPONSE_FAIL.status_code_string,
            'message': f"fail to build response in '{caller_name}' function",
        }, ensure_ascii=False),
        "isBase64Encoded": False
    }
