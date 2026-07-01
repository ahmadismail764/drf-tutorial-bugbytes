from django.db import models

class RawProduct(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    main_category = models.CharField(max_length=255, null=True, blank=True)
    sub_category = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(max_length=500, null=True, blank=True)
    link = models.URLField(max_length=500, null=True, blank=True)
    ratings = models.FloatField(null=True, blank=True)
    no_of_ratings = models.IntegerField(null=True, blank=True)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    actual_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.name or "Unnamed Product"