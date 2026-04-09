# decorators.py

import logging
from functools import wraps

from .mongo_exceptions import APIException
from .mongo_responses import custom_response

logger = logging.getLogger(__name__)


def handle_api_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIException as e:
            return custom_response(message=e.message, code=e.code, **e.payload if e.payload else {})
        except ValueError as e:
            # 明确的值错误，视为客户端错误
            return custom_response(message=str(e), code=400)
        except Exception as e:
            if isinstance(e, (KeyboardInterrupt, SystemExit)):
                raise
            logger.exception("Unhandled error in API")
            return custom_response(message="Internal server error", code=500)

    return decorated_function
