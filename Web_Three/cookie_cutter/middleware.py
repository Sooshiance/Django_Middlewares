import json
import logging
from datetime import datetime, timedelta

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


logger = logging.getLogger(__name__)
