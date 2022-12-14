from django.db import models
from django.conf import settings


class Label_attachment(models.Model):
    files = models.FileField(upload_to='uploads/label/')
    description = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='label_create_at')  # 建立者
