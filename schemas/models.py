from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class SchemaModelStatusChoices:
    READY = "Ready"
    PROCESSING = "Processing"
    FAILED = "Failed"

    CHOICES = (
        (READY, "Ready to download"),
        (PROCESSING, "In progress"),
        (FAILED, "Error"),
    )


class ColumnTypeChoices:
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


class SchemaModel(models.Model):
    """
    Model to represent a Schema instance
    """

    name = models.CharField("Name", max_length=255)
    separator = models.CharField("Separator", max_length=1, default=',')
    status = models.CharField(
        "Status", choices=SchemaModelStatusChoices.CHOICES, max_length=255
    )
    created_at = models.DateTimeField("Created at ", auto_now_add=True)

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
        ordering = ['-created_at']

    def __str__(self):
        return f"The schema {self.name} created at {self.created_at}"


class SchemaFile(models.Model):
    """
    File model with its status and creation date
    """
    file = models.FileField("Schema", blank=True, null=True, upload_to="media/")
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE, related_name='files')
    status = models.CharField(
        "File status", choices=SchemaModelStatusChoices.CHOICES, max_length=255, null=True, blank=True
    )
    created_at = models.DateTimeField("Created at ", auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def get_file_name(self):
        return 'media' + self.file.file


class ColumnModel(models.Model):
    """
    Model representing a column in the schema instance
    """

    name = models.CharField("Name", max_length=255)
    type = models.CharField(
        "Column type", max_length=30, choices=ColumnTypeChoices.CHOICES
    )
    quantity_range_lower = models.PositiveSmallIntegerField(
        "From", null=True, blank=True
    )
    quantity_range_upper = models.PositiveSmallIntegerField(
        "To", null=True, blank=True
    )
    order = models.PositiveSmallIntegerField(
        "Column order", default=1, validators=[MinValueValidator(1)]
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

