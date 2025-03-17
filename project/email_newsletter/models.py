from django.db import models
from datetime import datetime

class Appointment(models.Model):
    date = models.DateField(default=datetime.utcnow)  # Дата записи
    client_name = models.CharField(max_length=200)  # Имя клиента
    message = models.TextField()  # Сообщение от клиента

    def __str__(self):
        return f'{self.client_name}: {self.message}'  # Возвращает строковое представление объекта