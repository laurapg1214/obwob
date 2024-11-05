from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    # unique identifier for each record
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # soft delete fields
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # flag record as deleted; keep in db
    def delete_record(self):
        # set the is_deleted flag & deleted_at timestamp
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save() # save the changes instead of deleting

    # restore soft deleted records
    def restore(self):
        # remove the is_deleted flag & deleted_at timestamp
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    # override default delete method to prevent hard deletes
    def delete(self, *args, **kwargs):
        raise NotImplementedError(
            "Use delete_record() to perform a soft delete "
            "and keep the record in the database."
        )
    
    # filter soft deleted records
    # TODO: work out querying with relationships
    @classmethod
    def active_records(cls):
        return cls.objects.filter(is_deleted=False)

    def __str__(self):
        # return generic message as default
        return f"{self.__class__.__name__} instance"
    
    # make class abstract; won't create db table 
    class Meta:
        abstract = True  


# for coordinators to add custom fields to models (currently only for Participants)
class CustomField(BaseModel):
    # field types
    FIELD_TYPES = [
        ("TEXT", "Text"),
        ("NUMBER", "Number"),
        ("DATE", "Date"),
        # for choice options, see nested class CustomFieldChoice below
        ("CHOICE", "Choice"),
    ]

    name=models.CharField(max_length=100, verbose_name="Custom Field Name")
    type=models.CharField(
        max_length=10, 
        choices=FIELD_TYPES, 
        verbose_name="Custom Field Type"
    ) 
    value=models.TextField(verbose_name="Custom Field Value")
    is_valid=models.BooleanField(default=True, verbose_name="Is Valid")

    #TODO: implement client-side selection of model to attach custom field to using below booleans
    #TODO: implement server-side validation for field_value based on field_type
    is_participant_info=models.BooleanField(default=False)
    is_demographic=models.BooleanField(default=False)
    is_coordinator_info=models.BooleanField(default=False)
    is_event_info=models.BooleanField(default=False)
    is_facilitator_info=models.BooleanField(default=False)
    is_organization_info=models.BooleanField(default=False)
    is_question_info=models.BooleanField(default=False)
    is_reports_info=models.BooleanField(default=False)
    is_responses_info=models.BooleanField(default=False)

    class Meta:
        abstract = True

    # allows coordinators to provide choices in custom fields
    class CustomFieldChoice(BaseModel):
        # allow multiple choice options
        custom_field = models.ForeignKey(
            CustomField,
            on_delete=models.CASCADE,
            related_name="choices"
        )
        choice_text=models.CharField(max_length=250, verbose_name="Choice Text")
        is_valid=models.BooleanField(default=True, verbose_name="Is Valid")

        class Meta:
            abstract = True
            # ensure choices unique within each custom field
            unique_together = ("custom_field", "choice_text")
    


