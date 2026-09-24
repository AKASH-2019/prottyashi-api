# from rest_framework import serializers
# from .models import School


# class SchoolSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = School

#         fields = [
#             "id",
#             "school_code",
#             "emis_code",
#             "name_bn",
#             "student_count",
#             "active",
#             "created_at",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_at",
#             "updated_at",
#         ]

from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School

        fields = "__all__"

    def validate_student_count(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Student count must be greater than zero."
            )

        return value

class SchoolListSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = School
        fields = [
            "id",
            "school_code",
            "name_bn",
            "student_count",
        ]

class SchoolDetailSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = School
        fields = "__all__"