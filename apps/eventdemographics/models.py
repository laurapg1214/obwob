from apps.common.models import BaseModel
from apps.demographics.models import DemographicCategory
from apps.events.models import Event
from django.db import models

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