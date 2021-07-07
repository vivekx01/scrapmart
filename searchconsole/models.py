from django.db import models
class locality(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey("city", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % (self.name)


class city(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % (self.name)