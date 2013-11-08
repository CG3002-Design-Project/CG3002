from django.db import models

# Sample row 390791:8558:Salt & Pepper Fluted Mug:22814125:5:1/9/2013
class Transactions(models.Model):	
    transaction_id = models.DecimalField(max_digits=6,decimal_places=0)
    shop_id = models.DecimalField(max_digits=6,decimal_places=0)
    cashreg_id = models.DecimalField(max_digits=4,decimal_places=0)
    barcode = models.DecimalField(max_digits=8,decimal_places=0)
    qty = models.DecimalField(max_digits=5,decimal_places=0)
    sp = models.DecimalField(max_digits=5,decimal_places=2)
    purchase_date = models.DateField(auto_now=False,auto_now_add=False)
   