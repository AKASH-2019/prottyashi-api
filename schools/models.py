from django.db import models

# class School(models.Model):
#     school_code = models.CharField(max_length=20, unique=True)
#     emis_code = models.CharField(max_length=50, unique=True)

#     name_bn = models.CharField(max_length=255)

#     student_count = models.PositiveIntegerField()

#     active = models.BooleanField(default=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name_bn


class School(models.Model):
    school_code = models.CharField(
        max_length=20,
        unique=True
    )

    emis_code = models.CharField(
        max_length=50,
        unique=True
    )

    name_bn = models.CharField(
        max_length=255
    )

    student_count = models.PositiveIntegerField()

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.school_code} - {self.name_bn}"