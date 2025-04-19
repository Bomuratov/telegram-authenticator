# import logging
# from logging.config import dictConfig
# import re

# class MaskingFilter(logging.Filter):
#     def filter(self, record):
#         record.msg = self._mask_sensitive_info(str(record.msg))
#         return True

#     def _mask_sensitive_info(self, msg):
#         # Маскируем Telegram токены в URL (bot/123456789:AA... -> bot/***)
#         msg = re.sub(r'/bot/\d+:[\w-]+', '/bot/***', msg)

#         # Маскируем IP-адреса (10.214.171.132 -> 10.214.***.***)
#         msg = re.sub(r'(\d+\.\d+)\.\d+\.\d+', r'\1.***.***', msg)

#         return msg

# def setup_custom_logger():
#     dictConfig({
#         "version": 1,
#         "formatters": {
#             "default": {
#                 "format": "[%(asctime)s] [%(levelname)s] %(message)s",
#             },
#         },
#         "filters": {
#             "masking": {
#                 '()': MaskingFilter,
#             },
#         },
#         "handlers": {
#             "default": {
#                 "class": "logging.StreamHandler",
#                 "formatter": "default",
#                 "filters": ["masking"],
#             },
#         },
#         "loggers": {
#             "uvicorn": {
#                 "handlers": ["default"],
#                 "level": "INFO",
#             },
#             "uvicorn.access": {
#                 "handlers": ["default"],
#                 "level": "INFO",
#             },
#         },
#     })
