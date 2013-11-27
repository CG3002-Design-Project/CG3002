window.onload = function() {
	initSync();
}

function initSync(){
	$('#syncTransaction').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/transaction_sync",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
	$('#SyncInventory').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/inventory_sync",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
	$('#Restock').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/request_details_sync",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
	$('#SyncProduct').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/product_sync",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
	$('#productPull').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/pull_product_from_hq",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
	$('#inventoryPull').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/pull_inventory_from_hq",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
	$('#pricingStr').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/update_perishable_price",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
	$('#pricingStrPeri').click(function(){
	    console.log("reached add button click method");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/sync/update_nonperishable_price",
				success: function (response) {
					bootbox.alert("Transaction synced successfully");
				}
		});
    });
}