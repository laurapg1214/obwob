from apps.common.models import BaseModel
from apps.demographics.models import DemographicCategory
from apps.facilitators.models import Facilitator
from apps.organizations.models import Organization
from apps.participants.models import Participant
from apps.questions.models import Question
from apps.responses.models.import Response
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

    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    
    def __str__(self):
        return f"{self.name}, {self.date}" 
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
    

# mirrored in Rails PWA
class EventDemographicCategory(BaseModel):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name="event_demographic_categories"
    )
    category = models.ForeignKey(
        DemographicCategory, 
        on_delete=models.CASCADE, 
        related_name="event_demographic_categories"
    )
    
    def __str__(self):
        return f"{self.category} for {self.event}"
    
    class Meta:
        verbose_name = "Event Demographic Category"
        verbose_name_plural = "Event Demographic Categories"


# mirrored in Rails PWA
class EventFacilitator(BaseModel):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_facilitators"
    )
    facilitator = models.ForeignKey(
        Facilitator,
        on_delete=models.CASCADE,
        related_name="event_facilitators"
    )

    def __str__(self):
        return f"{self.facilitator} for {self.event}"
    
    class Meta:
        verbose_name = "Event Facilitator"
        verbose_name_plural = "Event Facilitators"
    

# mirrored in Rails PWA
class EventParticipant(BaseModel):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_participants"
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="event_participants"
    )

    def __str__(self):
        return f"{self.participant} for {self.event}"
    
    class Meta:
        verbose_name = "Event Participant"
        verbose_name_plural = "Event Participants"


# mirrored in Rails PWA
class EventQuestion(BaseModel):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_questions"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="event_questions"
    )

    def __str__(self):
        return f"{self.question} for {self.event}"
    
    class Meta:
        verbose_name = "Event Question"
        verbose_name_plural = "Event Questions"


# mirrored in Rails PWA
class EventResponse(BaseModel):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_responses"
    )
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="event_responses"
    )   

    def __str__(self):
        return f"{self.response} for {self.event}"
    
    class Meta:
        verbose_name = "Event Response"
        verbose_name_plural = "Event Responses"



