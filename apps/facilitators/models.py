from apps.common.models import BaseModel
from apps.organizations.models import Organization
from django.db import models


class Facilitator(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="facilitators"
    )
    
    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} - "
            f"Facilitator for {self.organization.name}"
        )
    
    class Meta:
        verbose_name = "Facilitator"
        verbose_name_plural = "Facilitators"
