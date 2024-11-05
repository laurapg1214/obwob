### ARCHIVED ###

from apps.common.models import BaseModel, PersonalInfoModel
from apps.common.utils import get_default_event
from apps.organizations.models import Organization
from django.core.exceptions import ValidationError
from django.db import models
import uuid


### CONTAINS Participant, Facilitator, CustomAttendeeType, EventAttendee ###

class EventAttendee(BaseModel):
    
    EVENT_ATTENDEE_TYPES = [
        ("PARTICIPANT", "Participant"),
        ("FACILITATOR", "Facilitator"),
        ("OTHER", "Other"), # custom types
    ]

    ### VALIDATION CHECK ###

    # validation check that facilitator's organization in event's organization(s)
    def clean(self):
        # map attendee types to their specific instances
        attendee_map = {
            "participant": self.participant,
            "facilitator": self.facilitator,
            "other": self.custom_attendee_type,
        }

        # get current attendee instance based on type
        attendee_instance = attendee_map.get(self.attendee_type)

        # conditional validation check if attendee instance exists
        if attendee_instance is not None:
            if attendee_instance.organization not in self.event.organizations.all():
                raise ValidationError(
                    f"{self.attendee_type.capitalize()} does not belong to any "
                    "of the organizations running the event"
                )
    
    # run validation on save
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    ### FIELDS ###    

    # PROTECT below for to maintain all events that were run and their attendees
    event = models.ForeignKey(
        # importing via string to avoid circular import
        "events.Event", 
        on_delete=models.PROTECT, 
        default=get_default_event,
        related_name="event_attendees"
    )
    # allows multiple orgs running an event to all have access to EventAttendees
    organizations = models.ManyToManyField(
        Organization,
        related_name = "event_attendees"
    )
    attendee_type = models.CharField(
        max_length=20, 
        choices=EVENT_ATTENDEE_TYPES,
        default="participant"
    )
    participant = models.ForeignKey(
        Participant, 
        null=True,
        blank=True, 
        on_delete=models.PROTECT, 
        related_name="event_attendees",
    )
    facilitator = models.ForeignKey(
        Facilitator, 
        null=True,
        blank=True, 
        on_delete=models.PROTECT,  
        related_name="event_attendees",
    )
    custom_attendee_type = models.ForeignKey(
        CustomAttendeeType,
        null=True,
        blank=True, 
        on_delete=models.PROTECT, 
        related_name="event_attendees",
    )
    registration_time = models.DateTimeField(auto_now_add=True)
    attendance_status = models.CharField(
        max_length=20, 
        choices=[
            ("ATTENDED", "Attended"), 
            ("ABSENT", "Absent")
        ], 
        default="attended"
    )

    def __str__(self):
        attendee = self.participant or self.facilitator or self.custom_attendee_type
        return f"{self.attendee_type.capitalize()}: {attendee} at {self.event}"

    class Meta:
        # avoid duplicate registrations: 
        # ensure each attendee assigned to specific event only once
        unique_together = (
            ("event", "participant"),
            ("event", "facilitator"),
            ("event", "custom_attendee_type", "participant"),
            ("event", "custom_attendee_type", "facilitator"),
        )
        verbose_name = "Event Attendee"
        verbose_name_plural = "Event Attendees"
        
    
