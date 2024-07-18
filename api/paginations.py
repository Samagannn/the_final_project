from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StadartPageNumberPagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 1000
