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
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     class Meta:
#         unique_together = (
#             "school",
#             "date"
#         )


class Delivery(models.Model):

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE
    )

    date = models.DateField()

    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    # Bun
    bun_delivered = models.PositiveIntegerField(default=0)
    bun_chalan_no = models.CharField(max_length=100, blank=True, null=True)
    bun_chalan_date = models.DateField(blank=True, null=True)
    bun_chalan_image = models.ImageField(
        upload_to="chalans/bun/",
        blank=True,
        null=True
    )

    # Egg
    egg_delivered = models.PositiveIntegerField(default=0)
    egg_chalan_no = models.CharField(max_length=100, blank=True, null=True)
    egg_chalan_date = models.DateField(blank=True, null=True)
    egg_chalan_image = models.ImageField(
        upload_to="chalans/egg/",
        blank=True,
        null=True
    )

    # Banana
    banana_delivered = models.PositiveIntegerField(default=0)
    banana_chalan_no = models.CharField(max_length=100, blank=True, null=True)
    banana_chalan_date = models.DateField(blank=True, null=True)
    banana_chalan_image = models.ImageField(
        upload_to="chalans/banana/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "school",
            "date"
        )

    def __str__(self):
        return f"{self.school.name_bn} - {self.date}"


class FoodPrice(models.Model):

    bun_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=22.883
    )

    egg_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=13.543
    )

    banana_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=9.807
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "Food Price Settings"