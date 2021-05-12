from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class SchemaModel(models.Model):
    """
    Model to represent a Schema instance
    """

    # status options
    READY = "Ready"
    PROCESSING = "Processing"
    FAILED = "Failed"

    CHOICES = (
        (READY, "Ready to download"),
        (PROCESSING, "In progress"),
        (FAILED, "Error"),
    )

    name = models.CharField("Name", max_length=255)
    separator = models.CharField("Separator", max_length=1, default=',')
    status = models.CharField(
        "Status", choices=CHOICES, max_length=255
    )
    created_at = models.DateTimeField("Created at ", auto_now_add=True)

    file = models.FileField("Schema", blank=True, null=True, upload_to="schemas/")
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="schemas",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Schema"
        verbose_name_plural = "Schemas"

    def __str__(self):
        return f"The schema {self.name} created at {self.created_at}"


class ColumnModel(models.Model):
    """
    Model representing a column in the schema instance
    """

    # column type options

    INT = "integer"
    DATE = "date"
    EMAIL = "email"
    PHONE = "phone"
    JOB = "job"

    CHOICES = (
        (INT, "Number range"),
        (DATE, "Date time"),
        (EMAIL, "E-mail"),
        (PHONE, "Phone number"),
        (JOB, "Job position"),
    )

    name = models.CharField("Name", max_length=255)
    type = models.CharField(
        "Column type", max_length=30, choices=CHOICES
    )
    order = models.PositiveSmallIntegerField(
        "Column order", default=1, validators=[MinValueValidator(1)]
    )
    quantity_range_lower = models.PositiveSmallIntegerField(
        "Нижняя граница диапазона чисел", null=True, blank=True
    )
    quantity_range_upper = models.PositiveSmallIntegerField(
        "Верхняя граница диапазона чисел", null=True, blank=True
    )
    schema = models.ForeignKey(
        SchemaModel,
        verbose_name="Schema",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="column_in_schemas",
    )

    class Meta:
        verbose_name = "Column in schema"
        verbose_name_plural = "Columns in schema"

    def __str__(self):
        return f"Column {self.name} in schema"

