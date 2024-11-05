from django.apps import apps
from django.shortcuts import render
from rest_framework import serializers, viewsets
import uuid


MODELS_LIST = [
    # "app_name", model_name
    # TODO insert authontication model
    ("coordinators", "Coordinator"),
    ("demographics", "DemographicCategory"),
    ("demographics", "Demographics"),
    ("organizations", "Organization"),
    ("questions", "Question"),
    # TODO insert reports model(s)
    ("events", "Event"), # dependencies on other serializers
    ]

CUSTOM_SERIALIZER_MODELS = [
    "EventAttendee",
]

### GENERATE SERIALIZERS & VIEWSETS ###
# generate_serializers & generate_viewsets called in 
# common.models BaseModelConfig
# attendee models use string import to avoid circular imports
# keep updated whenever custom serializer or viewset function added
def use_custom_serializer(model_name, serializers_dict):
    if model_name == "EventAttendee":
        return event_attendee_create_serializer()
    
    
def use_custom_viewset(model_name, serializers_dict):
    if model_name == "EventAttendee":
        return event_attendee_create_viewset()
    

### CUSTOM SERIALIZER FUNCTIONS ###
# dynamically add attendees during live event
def event_attendee_create_serializer(): 

    class EventAttendeeSerializer(serializers.ModelSerializer):

        class Meta:
            model = "attendees.EventAttendee"
            fields = [
                "event", 
                "organization", 
                "attendee_type", 
                "participant", 
                "facilitator", 
                "custom_attendee_type",
            ]
                      
        # allow coordinators to specify a custom_attendee_type when creating/updating attendees.
        # if the custom_attendee_type does not exist, create it
        custom_attendee_type = serializers.CharField(required=False)

        def create(self, validated_data):
            # validate organization exists in event
            event = validated_data["event"]
            custom_attendee_type_name = validated_data.pop("custom_attendee_type", None)

            # check if custom attendee type was provided
            if custom_attendee_type_name:
                custom_attendee_type, created = (
                    get_model("attendees", "CustomAttendeeType").objects.get_or_create(
                        type_name=custom_attendee_type_name,
                        # check if custom attendee type exists within event organization(s)
                        organization=event.organization
                    )
                )
                validated_data["custom_attendee_type"] = custom_attendee_type
            
            # call superclass create method to save EventAttendee
            return super().create(validated_data)

        def update(self, instance, validated_data):
            attendees_data = validated_data.pop("attendees", [])

            # create lists for both existing and new attendees, 
            # for bulk adding to minimize db hits
            attendees_to_create = []
            attendees_to_add = []

            for attendee_data in attendees_data:

                # extract attendee type model to avoid code duplication
                attendee_type = attendee_data.get("attendee_type")
                if attendee_type == "participant":
                    model = get_model("attendees", "Participant")
                elif attendee_type == "facilitator":
                    model = get_model("attendees", "Facilitator")
                else:
                    custom_attendee_type, _ = (
                       get_model("attendees", "CustomAttendeeType").objects.get_or_create(
                            type_name=attendee_type,
                            organization=instance.organization
                        )
                    )
                    # create an EventAttendee with this custom type
                    attendees_to_create.append(get_model("attendees", "EventAttendee")(
                        event=instance,
                        custom_attendee_type=custom_attendee_type,
                        unique_id=attendee_data.get("unique_id") or str(uuid.uuid4()),
                        first_name=attendee_data.get("first_name", ""),
                        last_name=attendee_data.get("last_name", ""),
                    ))
                    # skip to next attendee data
                    continue 
                    
                # for participant/facilitator, 
                # automatically assign a unique identifier if not provided
                unique_id = attendee_data.get("unique_id") or str(uuid.uuid4())
                
                # find or create the facilitator/participant
                attendee, created = model.objects.get_or_create(
                    unique_id=unique_id,
                    defaults={
                        "first_name": attendee_data.get("first_name", ""),
                        "last_name": attendee_data.get("last_name", "")
                    }
                )
                
                if created:
                    attendees_to_create.append(attendee)
                else:
                    attendees_to_add.append(attendee)

            # bulk create new attendees
            model.objects.bulk_create(attendees_to_create)

            # add new and existing attendees to the event
            if attendees_to_create or attendees_to_add:
                instance.attendees.add(*attendees_to_create, *attendees_to_add)
            
            return instance
        
    return EventAttendeeSerializer


### CUSTOM VIEWSET FUNCTION ###
def event_attendee_create_viewset():
    class EventAttendeeViewSet(viewsets.ModelViewSet):
        queryset = get_model("events", "Event").objects.all()
        serializer_class = event_attendee_create_serializer()

    return EventAttendeeViewSet