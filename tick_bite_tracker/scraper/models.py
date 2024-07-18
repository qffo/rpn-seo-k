from django.db import models


class TickBiteReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    cases = models.IntegerField()

    def __str__(self):
        return f'{self.start_date} - {self.end_date}: {self.cases} cases'
