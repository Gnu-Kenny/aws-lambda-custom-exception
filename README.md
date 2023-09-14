# AWS Lambda 내 사용자 정의 예외처리 도입

## 1, 가술스택

- Python3
- AWS Lambda(serverless)

## 2. 사용 목적

AWS 서버리스 아키텍쳐를 도입하고 서비스 개발을 진행하며 보다 다양한 종류의 예외처리가 가능해져야 했습니다.
특정 문제에 대한 명확한 이름을 가진 예외를 만들어 상세하고 정밀한 예외처리를 가능하게 하기 위해 도입하였습니다.

## 3. 동작 과정

1. 람다 호출시 핸들러에서 비즈니스 로직을 수행
2. 유효하지 못한 데이터의 접근으로 예외를 발생시, 사용자 정의 예외 호출
   ```python
    # lambda_handler.py
    
    # validate
    trigger = event['queryStringParameters']['trigger']
    if trigger not in ['Y', 'N']:
        raise CustomException(
            CommonResultCode.INVALID_PARAMETER,
            msg=f"Invalid query parameter, trigger must be 'Y' or 'N', {trigger}"
        )

   ```
3. 호출된 예외를 핸들러에서 캐치
   ```angular2html
    except Exception as exc:
        logger.info(exc)
        response = build_fail_response(exc)
   ```
4. CommonResultCode에서 설정한 상태코드와 에러 메세지를 Response DTO에 적용
   ```python
   # common/custom_response_builder
    def build_fail_response(err) -> dict:
        try:
            # lambda 의 response 형식 설정
            response = _init_json_response()
            
            if isinstance(err, CustomException):
                # CommonResultCode에 설정한 상태 코드 및 에러 메세지 적용
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
   ```


