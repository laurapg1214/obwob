from django.apps import apps
from django.shortcuts import render
from rest_framework import serializers, viewsets
import uuid


### SHARED FUNCTIONS ###
# default event = General Feedback
def get_default_event():
    # dynamically retrieve Event model to avoid AppRegistryNotReady error
    Event = get_model("events", "Event")
    return Event.objects.first() if Event.objects.exists() else None


# encapsulated views.py functionality with exception rendering custom error page
def get_object_or_error(
        request, 
        model, 
        object_id, 
        template_path, 
        extra_context=None, 
        event_name=None
        ):
    try:
        object = model.objects.get(pk=object_id)
        context_key = model.__name__.lower()
        context = {context_key: object}

        # merge extra_context, if provided, into context
        if extra_context:
            context.update(extra_context)

        return render(request, f"obwob/{template_path}", context)
    
    except model.DoesNotExist:
        requested_object = model.__name__.lower()
        return render(request, "obwob/404.html", {
            "error_message": f"Sorry, that {requested_object} does not exist."
        })
    

### MODELS/CUSTOM LISTS & FUNCTIONS for API layer automation of serializers, viewsets & URL registrations
MODELS_LIST = [
    # "app_name", model_name
    # TODO insert authentication model
    ("coordinators", "Coordinator"),
    ("demographics", "DemographicCategory"),
    ("demographics", "Demographics"),
    ("facilitators", "Facilitator"),
    ("organizations", "Organization"),
    ("participants", "Participant"),
    ("participants", "OtherParticipantType"),
    ("questions", "Question"),
    # TODO insert reports model(s)
    ("events", "Event"), # dependencies on other serializers
    ("events", "EventDemographicCategory"),
    ("events", "EventFacilitator"),
    ("events", "EventParticipant"),
    ("events", "EventQuestion"),
    ("events", "EventResponse"),
    ]

CUSTOM_SERIALIZER_MODELS = [
    "Event",
    # "EventParticipant",
]


# dynamically import models from specified app
def get_model(app_name, model_name):
    try:
        return apps.get_model(app_name, model_name)
    except LookupError:
        raise ValueError(f"Model {model_name} in app {app_name} not found.")


### GENERATE SERIALIZERS & VIEWSETS ###
# generate_serializers & generate_viewsets called in 
# common.models BaseModelConfig
# attendee models use string import to avoid circular imports
# keep updated whenever custom serializer or viewset function added
def use_custom_serializer(model_name, serializers_dict):
    if model_name == "Event":
        return event_create_serializer(serializers_dict) 
    #if model_name == "EventParticipant":
        #return event_participant_create_serializer()
    
    
def use_custom_viewset(model_name, serializers_dict):
    if model_name == "Event":
        return event_create_viewset(serializers_dict)
    #if model_name == "EventParticipant":
        #return event_participant_create_viewset()
    

### CUSTOM SERIALIZER FUNCTION ###
def event_create_serializer(serializers_dict):
    class EventSerializer(serializers.ModelSerializer):
        # get the EventAttendee serializer for attendees 
        #event_participant_serializer = serializers_dict.get(("events", "EventParticipant"))(many=True)
        #if event_participant_serializer is None:
            #raise ValueError("EventParticipant serializer not found")

        # get the Questions serializer for questions
        questions_serializer = serializers_dict.get(("questions", "Question"))(many=True)
        if questions_serializer is None:
            raise ValueError("Questions serializer not found")

        class Meta:
            model = get_model("events", "Event")
            fields = "__all__"

        def create(self, validated_data):
            # extract attendees and questions data if present
            #participants_data = validated_data.pop("participants", []) 
            questions_data = validated_data.pop("questions", [])

            # create the event object
            event = get_model("events", "Event").objects.create(**validated_data) 

            # prepare lists for bulk creation
            #participants_to_add = []
            questions_to_add = []

            # add participants to the event
            # for participant_data in participants_data:
            #     participant_type = participant_data.get("participant_type")

                # map participants to models for condensed code
                # TODO: work out new mapping below
                # participant_model_mapping = {
                #     "participant": "attendees.Participant",
                #     "facilitator": "attendees.Facilitator"
                # }

                # check for attendee type from standard models
            #     if attendee_type in attendee_model_mapping:    
            #         attendee_model = attendee_model_mapping[attendee_type]
            #         attendee, created = attendee_model.objects.get_or_create(id=attendee_data["id"])
            #         attendees_to_add.append("attendees.EventAttendee"(
            #             event=event,
            #             attendee_type=attendee_type,
            #             **{attendee_type: attendee} # dynamic field assignment **unpacking dict
            #         )) 

            #     # check for custom attendee type
            #     elif (custom_type_name := attendee_data.get("custom_attendee_type")):
            #         # check if custom type already exists for organization
            #         organization = event.organization
            #         custom_attendee_type, created = (
            #             "attendees.CustomAttendeeType".objects.get_or_create(
            #                 organization=organization, 
            #                 name=custom_type_name
            #             )
            #         )
            #         # assign custom type to attendee_type
            #         attendee_type = custom_attendee_type

            # # bulk add attendees to event to minimise db hits
            # if attendees_to_add:
            #     "attendees.EventAttendee".objects.bulk_create(attendees_to_add)

            # add questions to the event
            for question_data in questions_data:
                # check if the question already exists
                question_id = question_data.get("id")
                if question_id:
                    question, created = get_model(
                        "questions", "Question"
                    ).objects.get_or_create(
                        id=question_data["id"]
                    ) 
                else: 
                    question = get_model(
                        "questions", "Question"
                    ).objects.create(
                        **question_data
                    )
                    
                questions_to_add.append(question) 

            # bulk add questions to event to minimise db hits
            if questions_to_add:
                event.questions.add(*questions_to_add)
            
            return event
    
    return EventSerializer


### CUSTOM VIEWSET FUNCTION ###
def event_create_viewset(serializers_dict):
    class EventViewSet(viewsets.ModelViewSet):
        queryset = get_model("events", "Event").objects.all()
        serializer_class = event_create_serializer(serializers_dict)

    return EventViewSet

# TODO: add event_participant_create_serializer & event_participant_create_viewset


### DYNAMICALLY GENERATE SERIALIZERS ###
def generate_serializers():
    serializers_dict = {}

    for app_name, model_name in MODELS_LIST:
        model = get_model(app_name, model_name)
        
        # check for custom serializer
        if model_name in CUSTOM_SERIALIZER_MODELS:
            serializers_dict[
                (app_name, model_name)
            ] = use_custom_serializer(model_name, serializers_dict)
            continue

        # create Meta class dynamically
        meta_class = type(
            # model name
            "Meta",
            # tuple containing base class (comma ensures treated as a tuple)
            (object,),
            # dictionary defining class attributes
            {
                "model": model,
                "fields": "__all__"
            }
        )

        # create serializer class dynamically
        serializer_class = type(
            f"{model_name}Serializer", 
            (serializers.ModelSerializer,), 
            {
                "Meta": meta_class
            }
            )
        serializers_dict[(app_name, model_name)] = serializer_class
    
    return serializers_dict


### DYNAMICALLY GENERATE VIEWSETS ###
def generate_viewsets(serializers_dict):
    viewsets_dict = {}

    for (app_name, model_name), serializer_class in serializers_dict.items():
        model = get_model(app_name, model_name)

        # check for custom serializer:
        if model_name in CUSTOM_SERIALIZER_MODELS:
            viewset_class = use_custom_viewset(model_name, serializers_dict)
        else:
            viewset_class = type(
                f"{model_name}ViewSet", 
                (viewsets.ModelViewSet,), 
                {
                    "queryset": model.objects.all(),
                    "serializer_class": serializer_class
                })

        viewsets_dict[model_name] = viewset_class

    return viewsets_dict
        
