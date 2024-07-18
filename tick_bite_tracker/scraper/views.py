from django.shortcuts import render
from .models import TickBiteReport
import matplotlib.pyplot as plt
import io
import urllib
import base64



def index(request):
    reports = TickBiteReport.objects.all()
    dates = [report.start_date for report in reports]
    cases = [report.cases for report in reports]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, cases, marker='o')

    # Добавление цифр рядом с маркерами
    # +5 подняли цифры выше на 5
    for i in range(len(dates)):
        plt.text(dates[i], cases[i]+5, str(cases[i]), ha='center', va='bottom')

    plt.title('Количество случаев укуса Клеща с течением времени')
    plt.xlabel('Дата')
    plt.ylabel('Случаи')
    plt.grid(True)  # Включить сетку на графике

    # Осветлить границы
    plt.gca().spines["top"].set_alpha(.0)
    plt.gca().spines["bottom"].set_alpha(.3)
    plt.gca().spines["right"].set_alpha(.0)
    plt.gca().spines["left"].set_alpha(.3)
    


    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'scraper/index.html', {'data': uri})
