from rest_framework.pagination import LimitOffsetPagination


class CustomOffsetPagination(LimitOffsetPagination,):
    default_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 1000

    def get_paginated_response(self, data):
        data = {
                'data': data,
                'page': {
                    'links': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link()
                    },
                    'count': self.count
                }

        }
        return data
