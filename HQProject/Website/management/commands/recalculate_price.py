from django.core.management.base import BaseCommand, CommandError
from Website.models import Store,Product,Inventory,Transaction
from decimal import *

class Command(BaseCommand):
   #args = '<product_id batch_id product_id batch_id ...>'
    help = 'Runs pricing strategy on each product in Inventory'

    def handle(self, **options):
        inventory_list=Inventory.objects.all
        for curr_inventory in inventory_list():
            if curr_inventory.qty == 0:
                curr_inventory.selling_price+=(curr_inventory.selling_price)*curr_inventory.pricing_strategy
            else:
                curr_inventory.selling_price=Decimal(1.05)*curr_inventory.cost_price
            curr_inventory.save()
        # TODO Add logging here?

# To set this up:
# 1. Create file pricing_strategy_cronjob
# 2. In the file, add below line 
# 0 0 * * 0-6 python manage.py recalculate_price 
# (min hr day month day_run Command) << File format, this job runs recalculate_price.py every day at 12am
# 3. On Unix system, run this to set it up: crontab -a pricing_strategy_cronjob 