"""
    Generic Exception handler for DRF
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist):
        return Response(str(exc), status=status.HTTP_404_NOT_FOUND)

    if response is None:
        if hasattr(exc, 'code'):
            error = {'detail': exc.message,
                     'code': exc.code}
            if hasattr(exc, 'params') and getattr(exc, 'params', None):
                error['params'] = exc.params
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return None

    if 'detail' in response.data:
        if hasattr(response.data['detail'], 'code'):
            code = response.data['detail'].code
        else:
            code = 100

        response.data = [{
            "message": response.data['detail'],
            "code": code
        }]

    else:
        error_list = []
        for field, values in response.data.items():
            if isinstance(values, list):
                values = values[0]
                error = {
                    "field": field,
                    "message": str(values),
                    "code": getattr(values, 'code', 500)
                }
                error_list.append(error)

            else:
                error = {
                    "field": field,
                    "message": values.get(
                        'message', 'Internal Error 1.'),
                    "code": int(values.get('code', 500))
                }
                error_list.append(error)

        response.data = error_list
    return response
