from django.db import models
from django.conf import settings 

class RationSetting(models.Model):

    bun_per_student = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    egg_per_student = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    banana_per_student = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    effective_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Ration - {self.effective_date}"


class Holiday(models.Model):

    date = models.DateField(
        unique=True
    )

    title = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.date} - {self.title}"


# class Delivery(models.Model):

#     school = models.ForeignKey(
#         "schools.School",
#         on_delete=models.CASCADE
#     )

#     date = models.DateField()

#     bun_delivered = models.PositiveIntegerField()

#     egg_delivered = models.PositiveIntegerField()

#     banana_delivered = models.PositiveIntegerField()

#     chalan_photo = models.ImageField(
#         upload_to="chalans/"
#     )

#     entered_by = models.ForeignKey(
#         "accounts.User",
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("school", "date")


class Delivery(models.Model):

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE
    )

    date = models.DateField()

    bun_delivered = models.PositiveIntegerField()

    egg_delivered = models.PositiveIntegerField()

    banana_delivered = models.PositiveIntegerField()

    chalan_photo = models.ImageField(
        upload_to="chalans/"
    )

    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            "school",
            "date"
        )