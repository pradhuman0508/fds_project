from djongo import models

# Create your models here.
class Location(models.Model):
    # _id=models.AutoField(primary_key=True,editable=False,auto_created=True)
    id=models.ObjectIdField()
    location_name = models.CharField(blank=True, default=1,max_length=500)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_modified_datetime = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    license = models.IntegerField(default=0)


    def __str__(self):
        return self.location_name