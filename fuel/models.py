from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True)
    car_number = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class FuelRecord(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    distance = models.FloatField()
    fuel_amount = models.FloatField()
    cost = models.IntegerField(default=0) # ★この行が重要！
    efficiency = models.FloatField()
    weather_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.car.name}"
