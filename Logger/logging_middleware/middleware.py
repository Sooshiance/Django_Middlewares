import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin
from django.db.models.query import QuerySet


logger = logging.getLogger('django')


class UserActionsLogging(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Call the view function
        response = self.get_response(request)

        t1 = datetime.now()

        logger.info(response.headers)

        logger.info(f'Requested URL ===== : {request.path}')

        # Log the data loaded from the database
        # Note: This assumes that your view attaches the queryset to the request object
        # Check if the queryset attribute is set and log accordingly
        if hasattr(request, 'queryset'):
            if isinstance(request.queryset, QuerySet) and request.queryset is not None:
                # It's a queryset, log the query
                logger.info(f'user session ======= {request.session.session_key}')
                logger.info(f'Query Data loaded ====== {request.queryset.query}')
            else:
                # It's a single object, log the object's representation
                logger.info(f'user session ======= {request.session.session_key}')
                logger.info(f'Single Data loaded ====== {request.queryset}')

        t2 = datetime.now()

        # TODO: calculate how long these operations will take long
        # and to make it more efficient
        print(f"Elapsed time ======= {t2-t1}")

        return response
