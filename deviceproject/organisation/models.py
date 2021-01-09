from djongo import models
from datetime import datetime
import uuid



# Create your models here.

# class Organisation(models.Model):
#     name = models.CharField(blank=True, default=1,max_length=500)
#     # id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4, editable=False)
#     # _id=models.AutoField(primary_key=True,editable=False,auto_created=True)
#     id=models.ObjectIdField()
#     is_active = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     last_modified_datetime = models.DateTimeField(auto_now_add=True,null=True, blank=True)

#     def __str__(self):
#         return self.name