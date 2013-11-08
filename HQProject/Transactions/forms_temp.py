from django import forms
from .models import Transactions

# Create the form class.
class TransactionsForm(ModelForm):
	class Meta:
		model = Transactions
		fields = [ 'transaction_id', 'cashreg_id', 'barcode', 'qty', 'sp', 'purchase_date']

# Creating a form 
form = TransactionsForm()

# Creating a form to change an existing transaction
Transactions = Transactions.objects.get(pk=1)
form = TransactionsForm(instance=transaction)

