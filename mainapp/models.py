from django.db import models


class Moment(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    city_name = models.CharField(max_length=50, blank=True, null=True)
    weather_description = models.CharField(max_length=100, blank=True, null=True)
    temp = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    humidity = models.FloatField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    del_flg = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Moment ID: " + str(self.id)
