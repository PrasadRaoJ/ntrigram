from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MyProfile(models.Model):
    user = models.ForeignKey(User,related_name='profile',on_delete=models.CASCADE)

    school_name = models.CharField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=120,blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    dob = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles%Y/%m/%d/',blank=True,null=True)
    

    class Meta:
        verbose_name = ("MyProfile")
        verbose_name_plural = ("MyProfile")

    def __str__(self):
        return self.user.email


class CollegeData(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='collegedata')
    gender = models.CharField(max_length=120)
    school_type = models.CharField(max_length=120)
    school_location = models.CharField(max_length=120)
    is_ib_candidate = models.CharField(max_length=120)
    ethnicity = models.CharField(max_length=120)
    major = models.CharField(max_length=120)
    class_rank = models.CharField(max_length=120)
    passout_year = models.CharField(max_length=120)
    weighted_gpa = models.CharField(max_length=120)

    sub_eng_h = models.CharField(max_length=120)
    sub_mat_h = models.CharField(max_length=120)
    sub_sci_h = models.CharField(max_length=120)
    sub_oth_h = models.CharField(max_length=120)
    sub_hist_h = models.CharField(max_length=120)
    sub_arts_h = models.CharField(max_length=120)
    sub_ele_h = models.CharField(max_length=120)

    sat_math = models.CharField(max_length=120)
    sat_ebread = models.CharField(max_length=120)
    sat_wrt_lng = models.CharField(max_length=120)
    sat_scores_from = models.CharField(max_length=120)
    
    act_comp = models.CharField(max_length=120)

    
    

    class Meta:
        verbose_name = ("CollegeData")
        verbose_name_plural = ("CollegeData")

    def __str__(self):
        return self.user.email



