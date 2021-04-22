from django.db import models
from dashboard.models import Pig

class FPMining(models.Model):
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE)
    support = models.FloatField()
    itemset = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.pig.nickname}    {self.support*100}%  {self.itemset}'