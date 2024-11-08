from .models import Event
# TODO: get_object_or_error from common.utils below
from apps.common.utils import generate_serializers
from apps.facilitator.models import Facilitator
from apps.participant.models import Participant
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from io import BytesIO
from .models import Event
import qrcode
from rest_framework import generics, viewsets


# generate qr code for facilitators/participants
def generate_qr_code(request, event_id, user_id, user_type):
    # map user type to corresponding model, get user
    if user_type == 'facilitator':
        user = get_object_or_404(Facilitator, id=user_id)
    elif user_type == 'participant':
        user = get_object_or_404(Participant, id=user_id)
    else:
        raise Http404('Invalid user type')

    # get the event
    event = get_object_or_404(Event, id=event_id)

    # generate data for the qr code
    qr_data = f"https://obwob.com/scan/{event.id}/{user.id}"

    # generate qr code
    img = qrcode.make(qr_data)

    # save qr code to memory and return as png
    # initialize in-memory byte stream where the image data will be saved
    img_io = BytesIO()
    # save image to the img_io buffer
    img.save(img_io)
    # move file pointer to beginning of buffer
    img_io.seek(0)

    return HttpResponse(img_io, content_type="image/png")


# get serializers_dict
serializers_dict = generate_serializers()


class EventCreateView(generics.CreateAPIView):
    # fetch all Event objects
    queryset = Event.objects.all()

    # points to custom Event Serializer in utils.py
    serializer_class = serializers_dict.get('Event')


### orig setup below (pre-SPA setup) ###

# def index(request):
#     question_list = Question.objects.all()
#     context = {
#         "question_list": question_list,
#     }
#     return render(request, "obwob/index.html", context)


# custom error page
# def custom_404_view(request):
#     context = {
#         'error_message': "Oops! The page you're looking for doesn't exist."
#     }
#     print('there should be an error message!')
#     return render(request, '404.html', context, status=404)


# functions below use custom encapsulated get_object_or_error function from common.utils:
# def get_object_or_error(request, model, object_id, template_path, extra_context=None):
# def event(request, event_id, event_name):
#     return get_object_or_error(request, Event, event_id, "event.html", event_name)


# def event_questions(request, event_id, event_name):
#     extra_context = {
#         "questions": Question.objects.filter(events=event_id)
#     }
#     return get_object_or_error(request, Event, event_id, "event_questions.html", extra_context, event_name)


# def responses(request, question_id):
#     question = Question.objects.get(pk=question_id)
#     extra_context = {
#         "responses": Response.objects.filter(questions=question)
#     }
#     return get_object_or_error(request, Question, question_id, "responses.html", extra_context)


