from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def build_conversation_response_data(self, base_data: dict, results: list) -> dict:
        paginated = self.get_paginated_response(results).data
        base_data.update({
            "messages": paginated["results"],
            "count": paginated["count"],
            "next": paginated["next"],
            "previous": paginated["previous"]
        })
        return base_data
