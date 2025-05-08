from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers

ErrorDetailSerializer = inline_serializer(
    name='ErrorDetail',
    fields={
        'code': serializers.CharField(default='SOME_ERROR_CODE'),
        'details': serializers.DictField(default={'message': 'Some error message.'}),
    },
)

StandardErrorSerializer = inline_serializer(
    name='StandardErrorResponse', fields={'errors': serializers.ListField(child=ErrorDetailSerializer)}
)

STANDARD_ERROR_RESPONSES = {
    400: OpenApiResponse(response=StandardErrorSerializer, description='Invalid Request.'),
    404: OpenApiResponse(response=StandardErrorSerializer, description='Appeal not found.'),
    500: OpenApiResponse(response=StandardErrorSerializer, description='Unexpected internal error.'),
}
