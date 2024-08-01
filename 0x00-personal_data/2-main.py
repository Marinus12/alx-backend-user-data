#!/usr/bin/env python3
"""
Main file
"""

import logging

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))

logger = get_logger()
message = "name=John;email=john.doe@example.com;phone=123-456-7890;ssn=123-45-6789;password=secret;"
logger.info(message)
