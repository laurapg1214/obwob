from apps.common.models import BaseModel
from apps.events.models import Event
from apps.organizations.models import Organization
from django.db import models
#TODO: need EventDemographic and Participant models from Rails


# store demographic categories with field type choices
class DemographicCategory(BaseModel):
    FIELD_TYPE_CHOICES = [
        ("text", "Text"),
        ("number", "Number"),
        ("date", "Date"),
        ("choice", "Choice"),
    ]

    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name="demographic_categories"
    )
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPE_CHOICES)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Demographic Category"
        verbose_name_plural = "Demographic Categories"


# store demographic responses from participants
class Demographics(BaseModel):
    event_demographic = models.ForeignKey(
        EventDemographic, 
        on_delete=models.CASCADE, 
        related_name="demographics"
    )
    event_attendee = models.ForeignKey(
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
