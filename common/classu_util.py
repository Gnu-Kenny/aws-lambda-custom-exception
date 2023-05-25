from botocore.args import logger

from common.custom_response_builder import build_success_response, build_fail_response


def api_handler(func):
    """
    사용자 정의 예외 처리 데코레이터
    """

    def wrapper(*args, **kwargs):
        event = args[0]
        context = args[1]

        try:
            response_data = func(event, context)
            response = build_success_response(response_data)
        except Exception as exc:
            logger.exception("dump parameter", exc, event, context)
            response = build_fail_response(exc)

        return response

    return wrapper
