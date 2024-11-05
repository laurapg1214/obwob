from django.db import models


class AttendeeInfoModel(models.Model):
    # unique_id can be chosen by user or automatically assigned
    unique_id = models.CharField(max_length=50, unique=True, blank=True) 
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    # TODO from phonenumber_field.modelfields import PhoneNumberField
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    class CustomFieldValue(models.Model):
        CUSTOM_FIELD_TYPES = [
            ("text", "Text"),
            ("number", "Number"),
            ("date", "Date"),
            # for choice options, see class CustomFieldChoice below
            ("choice", "Choice"),
        ]

        attendee = models.ForeignKey(
            # string ref to avoid circular imports as defined w/in same class
            "AttendeeInfoModel",
            on_delete=models.CASCADE,
            related_name="custom_field_values"
        )
        field_name = models.CharField(max_length=100)
        field_type = models.CharField(max_length=10, choices=CUSTOM_FIELD_TYPES)
        value=models.TextField()

        class Meta:
            abstract = True
            unique_together = ("attendee", "field_name")

    # allows coordinators to provide choices in custom fields
    class CustomFieldChoice(models.Model):
        # allow multiple choice options
        custom_field_value = models.ForeignKey(
            "CustomFieldValue",
            on_delete=models.CASCADE,
            related_name="choices"
        )
        choice_text = models.CharField(max_length=100)
        # below: whether choice is currently valid/active; 
        # allows soft deletion without removing from db, and filtering for active
        is_valid = models.BooleanField(default=True)

        class Meta:
            abstract = True
            # ensure choices unique within each custom field
            unique_together = ("custom_field_value", "choice_text")

    class Meta:
        abstract = True  

