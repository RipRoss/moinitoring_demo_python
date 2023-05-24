from collections.abc import Mapping
import inspect
import logging
import logging.config
from typing import Any, Literal, Optional
from settings import VERSION, APP_NAME

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt: str | None = None, datefmt: str | None = None, style: Literal["%", "{", "$"] = "%", validate: bool = True, *, defaults: Mapping[str, Any] | None = None) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record):
        record.app = APP_NAME
        record.version = VERSION
        return super().format(record)


class CustomLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        """
        Intercept the log output and format the output accordingly.
        """
        ignore_fields = [
            "caller_lineno",
            "caller_filename",
            "rid"
        ]

        kwargs['extra']['custom_fields'] = " ".join([f"{key}=\"{value}\"" for key, value in kwargs['extra'].items() if key not in ignore_fields])
        return msg, kwargs


class Logger:
    def __init__(self, rid: Optional[str] = None) -> None:
        self.rid = rid
        logging.config.fileConfig('./config/logging.conf')
        logger = logging.getLogger()
        self.logger = CustomLogAdapter(logger, {})

    def debug(self, msg: str, **kwargs) -> None:
        stack = inspect.stack()[1]
        self.logger.debug(msg, extra={**kwargs, 'rid': self.rid, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno})

    def info(self, msg: str, **kwargs) -> None:
        stack = inspect.stack()[1]
        self.logger.info(msg, extra={**kwargs, 'rid': self.rid, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno})
    
    def warn(self, msg: str, **kwargs) -> None:
        stack = inspect.stack()[1]
        self.logger.warn(msg, extra={**kwargs, 'rid': self.rid, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno})
    
    def error(self, msg: str, **kwargs) -> None:
        stack = inspect.stack()[1]
        self.logger.error(msg, extra={**kwargs, 'rid': self.rid, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno})
    
    def critical(self, msg: str, **kwargs) -> None:
        stack = inspect.stack()[1]
        self.logger.critical(msg, extra={**kwargs, 'rid': self.rid, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno})

#     # these methods are required as the kwargs can only cointain certain key/value fields, one being `extra`. We create an interface that accepts any key/value pair, which is just more simple/native
# def debug(msg, **kwargs):
#     stack = inspect.stack()[1]
#     LOG_ADAPTER.debug(msg, extra={**kwargs, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno})


# def info(msg, *kwargs):
#     stack = inspect.stack()[0]
#     LOG_ADAPTER.info(msg, LOG_ADAPTER.debug(msg, extra={**kwargs, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno}))


# def warn(msg, *kwargs):
#     stack = inspect.stack()[0]
#     LOG_ADAPTER.warn(msg, LOG_ADAPTER.debug(msg, extra={**kwargs, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno}))


# def error(msg, *kwargs):
#     stack = inspect.stack()[0]
#     LOG_ADAPTER.error(msg, LOG_ADAPTER.debug(msg, extra={**kwargs, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno}))


# def critical(msg, *kwargs):
#     stack = inspect.stack()[0]
#     LOG_ADAPTER.critical(msg, LOG_ADAPTER.debug(msg, extra={**kwargs, 'caller_filename': stack.filename.split("/")[-1], 'caller_lineno': stack.lineno}))