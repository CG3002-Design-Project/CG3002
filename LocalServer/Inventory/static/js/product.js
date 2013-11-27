window.onload = function() {
	initEditProduct();
}

function validProduct(name,min_restock,manufacturer,category) {
	if (min_restock.length == 0){
		bootbox.alert('Invalid: Empty min_restock field');
		return false;
	}
	if (min_restock < 0 || min_restock > 99999){
		bootbox.alert('Invalid minimum restock value');
		return false;
	}
	if(manufacturer.trim().length > 40) {
		bootbox.alert("manufacturer cannot exceed 40 characters");
		return false;
	}
	if (category.trim().length > 40)
	{
		bootbox.alert('category cannot exceed 40 characters');
		return false;
	}
	if(name.trim().length > 40) {
		bootbox.alert('name cannot exceed 40 characters');
		return false;
	}
	return true;
	}

function edit_product(product_id,name,min_restock,manufacturer,category,status) {
		if(validProduct(name,min_restock,manufacturer,category)) {
			console.log("valid");
			$.ajax({url: "http://127.0.0.1:8000/Inventory/product/update_product",
					type: 'POST',
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					data:JSON.stringify({
						"product_id":product_id,
						"name":name,
						"min_restock":min_restock,
						"manufacturer":manufacturer,
						"category":category,
						"status":status,
					}),
					success: function (data) {
						console.log("here");
						bootbox.alert("Edited Successfully!", function() {
						  document.location.href="http://127.0.0.1:8000/Inventory/product";
						});
					}
			});
	}		
}
			
	

function initEditProduct(){
	$('#editProduct').click(function(){
	    console.log("reached add button click method");
		var product_id = $('#product_id').val();
		var name = $('#name').val();
		var min_restock = $('#min_restock').val();
		var manufacturer = $('#manufacturer').val();
		var category = $('#category').val();
		var status = $('#status').val();
		edit_product(product_id,name,min_restock,manufacturer,category,status);
    });
	
	$('#cancel').click(function(){
	    console.log("refresh display is clicked");
		document.location.href="http://127.0.0.1:8000/Inventory/inventory";
    });
}

