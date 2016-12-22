from django.db import models


class BaseModel(models.Model):
    """
    data의 작성일과 수정일을 module 화
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
