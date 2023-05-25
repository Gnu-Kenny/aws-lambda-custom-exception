from __future__ import annotations

import inspect

from common.ResultCode import ResultCode


class CustomException(RuntimeError):
    def __init__(self, result_code: ResultCode, msg: str = None):
        super().__init__(result_code, msg)

        self.result_code = result_code
        self.context = inspect.stack()

        if msg is not None:
            self.msg = msg
        else:
            self.msg = result_code.message
