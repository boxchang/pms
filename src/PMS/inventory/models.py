from django.db import models
from django.conf import settings
from datetime import datetime

from django.urls import reverse

from users.models import Unit


class FormStatus(models.Model):
    status_name = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='form_status_create_by')  # 建立者

    def __str__(self):
        return self.status_name


class ItemCategory(models.Model):
    catogory_code = models.CharField(max_length=2, blank=False, null=False)
    category_name = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='item_category_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_category_update_by')

    def __str__(self):
        return self.category_name


class ItemType(models.Model):
    category = models.ForeignKey(
        ItemCategory, related_name='item_category_type', on_delete=models.CASCADE)
    type_code = models.CharField(max_length=2, blank=False, null=False)
    type_name = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='item_type_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_type_update_by')

    def __str__(self):
        return self.type_name


class Item(models.Model):
    item_code = models.CharField(max_length=10, blank=False, null=False)
    sap_code = models.CharField(max_length=20, blank=True, null=True)
    vendor_code = models.CharField(max_length=20, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=False, null=False)
    item_type = models.ForeignKey(ItemType, related_name='item_type', on_delete=models.CASCADE)
    spec = models.CharField(max_length=2000, blank=True, null=True)
    price = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_update_by')

    def __str__(self):
        return self.spec

class Pic_attachment(models.Model):
    asset = models.ForeignKey('Item', related_name='item_pics', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/picture/item/')
    description = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_pic_create_by')  # 建立者


class AppliedForm(models.Model):
    form_no = models.AutoField(primary_key=True)
    unit = models.ForeignKey(Unit, related_name='applied_unit', on_delete=models.DO_NOTHING)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='applied_form_requester')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='applied_form_approver', blank=True, null=True)
    apply_date = models.CharField(max_length=10, blank=False, null=False, default=datetime.strftime(datetime.now(), "%Y-%m-%d"))
    status = models.ForeignKey(FormStatus, related_name='form_status', on_delete=models.DO_NOTHING)
    ext_number = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=2000, blank=True, null=True)
    total = models.IntegerField(default=0)
    admin_comment = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='inv_form_create_by')  # 建立者

    def get_absolute_url(self):
        return reverse('inv_detail', kwargs={'pk': self.pk})


class AppliedItem(models.Model):
    applied_form = models.ForeignKey(AppliedForm, related_name='applied_form_item', on_delete=models.CASCADE)
    item_code = models.CharField(max_length=10)
    spec = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    qty = models.IntegerField(default=0)
    unit = models.CharField(max_length=10)
    amount = models.IntegerField(default=0)
    comment = models.CharField(max_length=2000, blank=True, null=True)
    received_qty = models.IntegerField(default=0)


class Series(models.Model):
    key = models.CharField(max_length=50, blank=False, null=False)
    series = models.IntegerField()
    desc = models.CharField(max_length=50, blank=True, null=True)