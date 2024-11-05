from apps.common.models import BaseModel
from apps.demographics.models import DemographicCategory
from apps.organizations.models import Organization
from apps.questions.models import Question
from django.db import models


class Event(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    organizations = models.ManyToManyField(
        Organization, 
        related_name="events" 
    )
    questions = models.ManyToManyField(
        Question, 
        blank=True,
        related_name="events" 
    )
    
    def __str__(self):
        return f"{self.name}, {self.date}" 
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
    

# link demographic categories with events
class EventDemographic(BaseModel):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name="event_demographics"
    )
    category = models.ForeignKey(
        DemographicCategory, 
        on_delete=models.CASCADE, 
        related_name="event_demographics"
    )
    
    def __str__(self):
        return f"{self.category} for {self.event}"
    
    class Meta:
        verbose_name = "Event Demographic"
        verbose_name_plural = "Event Demographics"


# TODO: add EventParticipant model


# TODO: add EventResponse model



