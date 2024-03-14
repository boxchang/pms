from django.db import models
from django.conf import settings


class Storage(models.Model):
    storage_code = models.CharField(max_length=6, primary_key=True)
    desc = models.CharField(max_length=200, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='storage_update_by')
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.desc


class Location(models.Model):
    storage = models.ForeignKey(Storage, related_name='storage_location', on_delete=models.DO_NOTHING)
    location_code = models.CharField(max_length=10, primary_key=True)
    location_name = models.CharField(max_length=20, blank=False, null=False)
    desc = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='location_update_by')

    def __str__(self):
        return self.desc


class Bin(models.Model):
    location = models.ForeignKey(Location, related_name='location_bin', on_delete=models.DO_NOTHING)
    bin_code = models.CharField(max_length=20, primary_key=True)
    bin_name = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='bin_update_by')

    def __str__(self):
        return self.bin_name
