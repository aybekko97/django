from django.db import models

# Create your models here.


class CompanyManager(models.Manager):
    def get_confirmed(self):
        return super(CompanyManager, self).get_queryset().filter(status=Company.Status.CONFIRMED)

    def get_waiting(self):
        return super(CompanyManager, self).get_queryset().filter(status=Company.Status.WAITING)


class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"
    class Status:
        WAITING = 0
        CONFIRMED = 1
    name = models.CharField(max_length=50)
    token = models.CharField(max_length=30, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    status = models.IntegerField(default=Status.WAITING)

    objects = CompanyManager()

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.id, self.name, self.phone)
