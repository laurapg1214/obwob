from . import views
from django.urls import path
# TODO: check necessity of below
from .views import EventCreateView

app_name = 'events'

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
    path(
        'generate_qr/<uuid:event_id>/<uuid:user_id>/<str:user_type>',
         views.generate_qr_code,
         name='generate_qr_code'
    ),
    path(
        'generate_qr/<uuid:event_id>/<uuid:participant_id>/',
         views.generate_participant_qr,
         name='generate_participant_qr'
    ),
]



