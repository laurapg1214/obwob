from apps.common.models import BaseModel, CustomField
from apps.organizations.models import Organization
from apps.participants.models import Participant
from django.db import models


# TODO: add default demographic categories
# store demographic categories with field type choices
class DemographicCategory(BaseModel):
    custom_fields = models.ManyToManyField(
        CustomField, 
        blank=True, 
        related_name="demographic_categories"
    )
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name="demographic categories"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Demographic Category"
        verbose_name_plural = "Demographic Categories"


# store demographic responses from participants
class Demographics(BaseModel):
    DemographicCategory = models.ForeignKey(
        DemographicCategory, 
        on_delete=models.CASCADE, 
        related_name="demographics"
    )
    participant = models.ForeignKey(
        Participant,
        null=True, 
        blank=True,
        on_delete=models.CASCADE,
        related_name="demographics"
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"Response for {self.event_demographic.category} "
            "by {self.event_attendee}"
        )
    
    class Meta:
        verbose_name = "Demographic"
        verbose_name_plural = "Demographics"
