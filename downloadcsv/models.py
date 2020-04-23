from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
# from django.conf import settings

# Create your models here.
class Metadata(models.Model):
    node_id = models.IntegerField(unique=True, primary_key=True, null=True)
    Building_Name = models.CharField(max_length=255, null=True)
    Start_Date = models.DateField(max_length=255, null=True)
    Consumption = models.CharField(max_length=255, null=True)
    Units = models.CharField(max_length=255, null=True)



class YearlyResult(models.Model):
    node_id = models.ForeignKey(Metadata, on_delete=models.CASCADE)
    rating = models.FloatField()
    date = models.DateField()
    time = models.TimeField()


# class NodeDetail(models.Model):
#     node_id = models.IntegerField()  # primary key.
#     department_name = models.CharField(max_length=200)
#     building_name = models.CharField(max_length=200)





# class User(AbstractUser):
#     username = models.CharField (blank=True, null=True)
#     email = models.EmailField(_('email address'), unique=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     def __str__(self):
#         return "{}".format(self.email)
#
# class UserProfile(models.Model):
#     user = models.OneToOneField (settings.AUTH_USER_MODEL,
#     )




