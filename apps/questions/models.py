from apps.common.models import BaseModel
from apps.organizations.models import Organization
from django.db import models


class Question(BaseModel):
    text = models.CharField(max_length=255)
    organization = models.ForeignKey(
        Organization, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="questions", 
    )

    is_active = models.BooleanField(default=True, verbose_name="Is Active")
        
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
    
