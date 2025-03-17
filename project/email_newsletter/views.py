from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail  # Импортируем функцию для отправки писем
from datetime import datetime
from .models import Appointment  # Импортируем модель Appointment

class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'email_newsletter/make_appointment.html', {})  # Отображаем форму для записи

    def post(self, request, *args, **kwargs):
        # Создаём объект Appointment из данных формы
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),  # Преобразуем строку в дату
            client_name=request.POST['client_name'],  # Имя клиента
            message=request.POST['message'],  # Сообщение от клиента
        )
        appointment.save()  # Сохраняем запись в базе данных

        # Отправляем письмо
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',  # Тема письма
            message=appointment.message,  # Сообщение
            from_email='djodiseq@yandex.ru',  # Адрес отправителя
            recipient_list=[]  # Список получателей
        )

        return redirect('appointments:make_appointment')  # Перенаправляем на страницу с формой