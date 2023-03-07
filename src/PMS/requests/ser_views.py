from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from requests.models import Request
from requests.serializers import RequestSerializer


class RequestByPViewSet(ListModelMixin, GenericViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(self):
        p_id = self.kwargs['project_id']
        exclude_list = ['6','8']
        queryset = Request.objects.filter(project=p_id, belong_to=None).exclude(exclude_list).order_by('level')

        return queryset


class SubRequestViewSet(ListModelMixin, GenericViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(self):
        r_id = self.kwargs['request_id']
        queryset = Request.objects.filter(belong_to=r_id)

        return queryset

