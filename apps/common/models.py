from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
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
