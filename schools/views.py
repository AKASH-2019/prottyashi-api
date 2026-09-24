from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .models import School
from .serializers import SchoolSerializer, SchoolListSerializer, SchoolDetailSerializer
from .permissions import SchoolPermission


class SchoolViewSet(viewsets.ModelViewSet):

    queryset = School.objects.all().order_by(
        "school_code"
    )

    serializer_class = SchoolSerializer

    permission_classes = [SchoolPermission]

    filter_backends = [SearchFilter]

    search_fields = [
        "school_code",
        "emis_code",
        "name_bn",
    ]


def get_queryset(self):

    queryset = School.objects.all()

    active = self.request.query_params.get(
        "active"
    )

    if active is not None:

        queryset = queryset.filter(
            active=active.lower() == "true"
        )

    return queryset.order_by(
        "school_code"
    )

def get_serializer_class(self):

    if self.action == "list":
        return SchoolListSerializer

    return SchoolDetailSerializer