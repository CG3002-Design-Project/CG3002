import django_filters

class ProductFilter(django_filters.FilterSet):
	class Meta:
        model = Product
        fields = ['product_id', 'name', 'min_restock', 'manufacturer', 'category', 'status']	

