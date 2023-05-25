from botocore.args import logger

from common.CommonResultCode import CommonResultCode
from common.CustomException import CustomException
from common.custom_response_builder import build_success_response, build_fail_response


# @api_handler
def lambda_handler(event, context):
    try:
        # validate
        trigger = event['queryStringParameters']['trigger']
        if trigger not in ['Y', 'N']:
            raise CustomException(
                CommonResultCode.INVALID_PARAMETER,
                msg=f"Invalid query parameter, trigger must be 'Y' or 'N', {trigger}"
            )

        # service
        if trigger == "Y":
            raise CustomException(CommonResultCode.RESOURCE_NOT_FOUND,
                                  msg=f"exception has occurred by trigger, {trigger}")

        # build response
        response_data = {
            "trigger": trigger
        }

        response = build_success_response(response_data)

    except Exception as exc:
        logger.info(exc)
        response = build_fail_response(exc)

    return response
