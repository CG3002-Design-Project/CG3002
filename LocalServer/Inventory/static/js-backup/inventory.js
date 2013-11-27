window.onload = function() {
	initEditInventory();
}

function validInventory(selling_price,minimum_qty,strategy_percentage) {
	if (selling_price.length == 0){
		bootbox.alert('Invalid: Empty selling price field');
		return false;
	}
	if(selling_price < 0 || strategy_percentage < 0  ) {
		bootbox.alert("selling price must be positive");
		return false;
	}
	if (strategy_percentage > 9999.99 || selling_price > 9999.99)
	{
		bootbox.alert('cannot exceed 9999.99');
		return false;
	}
	if(minimum_qty > 999999) {
		bootbox.alert('cannot exceed 999999');
		return false;
	}
	return true;
	}

function edit_inventory(product_id,batch_id,qty,cost_price,selling_price,minimum_qty,strategy_percentage,display_id,expiry_date) {
		if(validInventory(selling_price,minimum_qty,strategy_percentage)) {
			console.log("valid");
			$.ajax({url: "http://127.0.0.1:8000/Inventory/inventory/update_inventory",
					type: 'POST',
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					data:JSON.stringify({
						"product_id_id":product_id,
						"batch_id":batch_id,
						"qty":qty,
						"cost_price":cost_price,
						"selling_price":selling_price,
						"minimum_qty":minimum_qty,
						"strategy_percentage":strategy_percentage,
						"display_id" : display_id,
						"expiry_date" : expiry_date
					}),
					success: function (data) {
						console.log("here");
						bootbox.alert("Edited Successfully!", function() {
						  document.location.href="http://127.0.0.1:8000/Inventory/inventory";
						});
					}
			});
	}		
}
			
	

function initEditInventory(){
	$('#editInventory').click(function(){
	    console.log("reached add button click method");
		var product_id = $('#product_id_id').val();
		var batch_id = $('#batch_id').val();
		var qty = $('#qty').val();
		var cost_price = $('#cost_price').val();
		var selling_price = $('#selling_price').val();
		console.log(selling_price);
		var minimum_qty = $('#minimum_qty').val();
		var strategy_percentage = $('#strategy_percentage').val();
		var display_id = $('#display_id').val();
		var expiry_date = $('#expiry_date').val();
		edit_inventory(product_id,batch_id,qty,cost_price,selling_price,minimum_qty,strategy_percentage,display_id,expiry_date);
    });
}

