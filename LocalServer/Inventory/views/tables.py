# tutorial/tables.py
import django_tables2 as tables
from Inventory.models import Product,Inventory
from django_tables2.utils import A 

TEMPLATE = """
<input id="count" maxlength="100" name="count" type="text"/>
"""
class ProductTable(tables.Table):
	product_id = tables.LinkColumn('edit_product', args=[A('product_id')])
	class Meta:
		model = Product
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}

class InventoryTable(tables.Table):
	id = tables.TemplateColumn(TEMPLATE)
	class Meta:
		model = Inventory
		# add class="paleblue" to <table> tag
		attrs = {"class": "bordered"}