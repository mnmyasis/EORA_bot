import json
from http import HTTPStatus

from django.urls import reverse

from .models import ChatHistory, BaseStatistic

BASE_STATISTIC_URLS = (
    reverse('api:message_view'),
)


def log_middleware(get_response):
    def middleware(request):
        request_body = request.body
        response = get_response(request)
        if request.path == reverse('api:message_view'):
            if (request.method == 'POST' and
                    HTTPStatus.OK == response.status_code):
                body = json.loads(request_body)
                ChatHistory.objects.create(
                    user=body.get('user_id'),
                    message=body.get('message'),
                    answer=response.data.get('text')
                )
        return response

    return middleware


def base_statistic_middleware(get_response):
    def middleware(request):
        if request.path in BASE_STATISTIC_URLS:
            ip_address = request.META.get('REMOTE_ADDR')
            browser = request.META.get('HTTP_USER_AGENT')
            params = request.META.get('QUERY_STRING')
            BaseStatistic.objects.create(
                ip_addr=ip_address,
                browser=browser,
                request_params=params
            )
        response = get_response(request)
        return response

    return middleware
