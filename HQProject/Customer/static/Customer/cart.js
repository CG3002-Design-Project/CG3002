var cashier = 3002;
var itemIdx = 0;
var totalPrice = 0;

window.onload = function() {
	initAddItem();
	initAddTransaction();
	initCancelItem();
}

function validItem(barcode, quantity, batchid) {
	var valid = true;
	if (barcode == '' || quantity == '' || batchid == '') {
		bootbox.alert('Cannot have empty fields only');
		valid = false;
	}
	if (!is_int(quantity)){
		bootbox.alert('Integers only');
		valid = false;
	} if (barcode.length != 8 || !is_int(barcode)) {
		bootbox.alert('Barcode has to be a valid 8 digit number');
		valid = false;
	} if (batchid.length  > 5 ||  !is_int(batchid)) {
		bootbox.alert("Batch id has to be a valid 5 digit number!!"); 
		valid = false;
	}
	if (parseInt(quantity)<0){
		bootbox.alert('Non-negative quantity only');
		valid = false;
	}
	return valid;
}

function is_int(value) { 
	if((parseFloat(value) == parseInt(value)) && !isNaN(value)){
		return true;
	} else { 
		return false;
	} 
}

function initCancelItem(){
	$('#cancel').click(function(){
	    console.log("lolita");
		document.location.href="http://127.0.0.1:8000/Inventory/transaction";
	});
}

function initAddItem(){
$('#add-item').click(function(){
		var barcode = $('#inputBarcode').val();
		console.log(barcode);
		var quantity = $('#inputQuantity').val();
		console.log(quantity);
		var batchid = $('#inputBatchID').val();
		console.log(batchid);
		if (validItem(barcode,quantity,batchid)) {
			$.ajax({
			url: 'http://127.0.0.1:8000/Inventory/returnPrice', 
			type: 'POST',
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data:JSON.stringify({'barcode' : barcode,'batchid': batchid, 'qty': quantity}),
			success: function (response) {
				if (response.error == 1){
					var unitprice = response.price;
					var collectiveprice = parseFloat(unitprice).toFixed(2) * parseInt(quantity);
					totalPrice = totalPrice + collectiveprice;
					$('#total-price').text(totalPrice);
					$('#item-table').append('<tr barcode="'+barcode+'" class="items" id="item-'+itemIdx+'">'+
					'<td>'+barcode+'</td>'+
					'<td>'+batchid+'</td>'+
					'<td>'+response.name+'</td>'+
					'<td>'+quantity+'</td>'+
					'<td>'+unitprice+'</td>'+
					'<td id="collective-'+itemIdx+'">'+collectiveprice+'</td>'+
					'<td><img onclick="removeItem('+itemIdx+')" src="/static/images/delete.png" style="cursor:pointer;" title="Delete item"/></td>');
					$('#new-item-form')[0].reset();
					itemIdx++;
				}
				else if(response.error == -2) {
					bootbox.alert("only " + response.qty + " products are available");
				} else {
					bootbox.alert('No such product exist');
				}
			}
		});
	}
});
}



function removeItem(index){

	var contents = $('td#collective-'+index).text();
	$('#item-'+index).remove();	
	totalPrice = totalPrice - parseFloat(contents).toFixed(2);
	$('#total-price').text(totalPrice);	
}

function initAddTransaction(){
	$('#confirm-checkout').click(function(){
		var itemList = [];
		$('.items').each(function(idx,item){
			var item_obj = new Object();
			item_obj.barcode = $(item).attr('barcode');
			item_obj.quantity = $(item).children()[1].textContent;
			item_obj.price = $(item).children()[2].textContent;
			itemList.push(item_obj);
		});
		$.ajax({
			url: "/processTransaction",
			type: 'POST',
			data: {
				"cashier":cashier,
				"list":itemList
			},
			success: function (response) {
				if (response.STATUS != "ERROR")	{
					initTable();
					$('#addNewTransaction').modal('hide');
					itemIdx = 0;
					$('.items').remove();
					totalPrice = 0;
					$('#total-price').text(totalPrice);	
				}
				else{
					alert("Error processing transaction");
					$('#addNewTransaction').modal('hide');
					itemIdx = 0;
					$('.items').remove();
					totalPrice = 0;
					$('#total-price').text(totalPrice);	
				}	
			}
		});

	});
}


	
