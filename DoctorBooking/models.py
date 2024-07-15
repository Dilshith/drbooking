from django.db import models

# Create your models here.

class login_table(models.Model):
    username  = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=10)


class doctor_reg_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    image = models.FileField()
    Designation = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    experience = models.CharField(max_length=115)
    phone = models.BigIntegerField()
    place = models.CharField(max_length=20)
    post = models.CharField(max_length=20)
    pin = models.CharField(max_length=20)


class user_reg_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    image = models.FileField()
    email = models.CharField(max_length=20)
    phone = models.BigIntegerField()
    place = models.CharField(max_length=20)
    post = models.CharField(max_length=20)
    pin = models.CharField(max_length=20)

class schedule_table(models.Model):
    date = models.DateField()
    DOCTOR = models.ForeignKey(doctor_reg_table, on_delete=models.CASCADE)
    fromtime = models.CharField(max_length=100)
    totime = models.CharField(max_length=100)


class booking_table(models.Model):
    date = models.DateField()
    time = models.TimeField()
    USER = models.ForeignKey(user_reg_table, on_delete=models.CASCADE)
    SCHEDULE = models.ForeignKey(schedule_table, on_delete=models.CASCADE)


class prescription_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    BOOKING = models.ForeignKey(booking_table, on_delete=models.CASCADE)
    image = models.FileField()
    notes = models.CharField(max_length=20)

class notification_table(models.Model):
    notification = models.CharField(max_length=20)
    date = models.DateField()



class user_rating_table(models.Model):
    rating = models.CharField(max_length=20)
    date = models.DateField()
    USER = models.ForeignKey(user_reg_table, on_delete=models.CASCADE)
    DOCTOR = models.ForeignKey(doctor_reg_table,on_delete = models.CASCADE)
