from rest_framework.generics import GenericAPIView


def make_bool(val):
    return val not in ['False', 'false', 0, '0', False]


class SerializerByMethodMixin:
    serializer_classes = None

    def get_serializer_class(self):
        if self.serializer_classes is not None:
            return self.serializer_classes.get(self.request.method.lower())
        return super().get_serializer_class()


class SerializerByActionMixin:
    serializer_classes = None

    def get_serializer_class(self):
        if self.serializer_classes is not None:
            if self.action == 'partial_update':
                return self.serializer_classes.get('update')
            return self.serializer_classes.get(self.action)
        return super().get_serializer_class()


class PaginationBreakerMixin:

    def paginate_queryset(self, queryset):
        use_pagination = make_bool(self.request.GET.get('use_pagination'))
        if not use_pagination:
            self.pagination_class = None

        return super().paginate_queryset(queryset)


class UltraGenericAPIView(SerializerByMethodMixin, PaginationBreakerMixin, GenericAPIView):
    pass