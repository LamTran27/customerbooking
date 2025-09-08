from django.db import models
from django.contrib.auth.models import User
import os
import uuid
from django.utils import timezone
from PIL import Image, ImageOps
# Create your models here.

class UserAccount(models.Model):
    STORE_CHOICES = [
        ('HDN', 'Honda Ô tô Đà Nẵng'),
        ('HQN', 'Honda Ô tô Quảng Nam'),
        ('TTQN', 'Toyota Quảng Ngãi'),
        ('TLQN', 'Toyota Trang Lê Quảng Nam'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    store = models.CharField(max_length=10, choices=STORE_CHOICES, default='')
    hotline = models.CharField(max_length=50, null=False, blank=False)
    isadmin = models.BooleanField(default=False)
    adddate = models.DateTimeField(auto_now_add=True)  
    lastupdateuserid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_accounts')
    lastupdatedate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tài khoản mở rộng của {self.user.username}"
    
class Customer(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)  # Tên khách hàng
    plate = models.CharField(max_length=50, null=False, blank=False)  # Biển số xe
    note = models.TextField(max_length=50, null=True, blank=True)     # Ghi chú
    adddate = models.DateTimeField(default=timezone.now, null=True, blank=True)              # Ngày thêm mới
    isdelete = models.BooleanField(default=False)                     # Đánh dấu đã xóa
    deletedate = models.DateTimeField(null=True, blank=True)          # Ngày xóa (nếu có)
    lastupdateuserid = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )                                                                 # Người cập nhật cuối
    lastupdatedate = models.DateTimeField(auto_now=True)             # Ngày cập nhật cuối
    KHDV = models.CharField(max_length=50, null=True, blank=True)     # Khách hàng dịch vụ
    CVDV = models.CharField(max_length=50, null=True, blank=True)     # Cố vấn dịch vụ

    def __str__(self):
        return f"{self.name} - {self.plate}"
    
def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('pictures/', new_filename)

class Pictures(models.Model):
    pictureName = models.ImageField(upload_to=upload_to)
    isDeleted = models.BooleanField(default=False)
    adddate = models.DateTimeField(default=timezone.now, null=True, blank=True)   
    deletedDate = models.DateTimeField(null=True, blank=True)
    lastupdateuserid = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )   
    lastUpdateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Picture {self.id}"
