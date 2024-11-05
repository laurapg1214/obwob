from apps.common.models import BaseModel, CustomField
from apps.organizations.models import Organization
from django.db import models


class Participant(BaseModel):
    # optional unique username
    username = models.CharField(max_length=50, unique=True, blank=True)
    # emoji for optional participant self-identification within workshop 
    emoji = models.CharField(max_length=10, blank=True) 
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    # TODO from phonenumber_field.modelfields import PhoneNumberField
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    custom_fields = models.ManyToManyField(
        CustomField, 
        blank=True, 
        related_name="participants"
    )

    participant_type = models.CharField(max_length=50, default="Participant")
    other_participant_type = models.ForeignKey(
        "OtherParticipantType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="participants"
    )

    # for archival preservation of deleted types in participant records
    archived_participant_type = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # set participant type to other_participant_type if it exists
        if self.other_participant_type:
            self.participant_type = self.other_participant_type.name
        # archive participant type before saving
        if self.participant_type:
            self.archived_participant_type = self.participant_type
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unique_id} {self.first_name} {self.last_name} - Participant"

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"


class OtherParticipantType (BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, blank=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="other_participant_types"
    )
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = "Other Participant Type"
        verbose_name_plural = "Other Participant Types"


