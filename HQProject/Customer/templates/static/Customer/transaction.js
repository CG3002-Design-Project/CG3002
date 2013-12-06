var cashier = 3002;
var itemIdx = 0;
var totalPrice = 0;

window.onload = function() {
	initAddItem();
	initAddTransaction();
}

function validItem(barcode, quantity, batchid) {
	var valid = true;
	if (barcode == '' || quantity == '' || batchid = '')
		valid = false;
	if (!is_int(quantity)){
		alert('Integers only')
		valid = false;
	} if (barcode.length != 8 || !is_int(barcode)) {
		alert('Barcode has to be a valid 8 digit number')
		valid = false;
	} if (batchid.length !=4 ||  !is_int(batchid)) {
		alert("Batch id has to be a valid 5 digit number!!"); 
		valid = false;
	}
	if (parseInt(quantity)<0){
		alert('Non-negative quantity only');
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

function initAddItem(){
$('#add-item').click(function(){
		var barcode = $('#inputBarcode').val();
		var quantity = $('#inputQuantity').val();
		var quantity = $('#inputBatchid').val();
		if (!validItem(barcode,quantity)){
			$('#prompt-error').show();
			return;
		}
		else
			$('#prompt-error').hide();
			$.ajax({
			url: 'http://127.0.0.1:8000/Inventory/returnPrice', 
			type: 'POST',
			data: {'barcode' : barcode,'batchid': batchid, 'qty': quantity}},
			success: function (response) {
				if (response.error == 1){
					var unitprice = response.price;
					var collectiveprice = parseFloat(unitprice).toFixed(2) * parseInt(quantity);
					totalPrice = totalPrice + collectiveprice;
					$('#total-price').text(totalPrice);
					$('#item-table').append('<tr barcode="'+barcode+'" class="items" id="item-'+itemIdx+'">'+
					'<td>'+batchid+'</td>'+
					'<td>'+response.name+'</td>'+
					'<td>'+quantity+'</td>'+
					'<td>'+unitprice+'</td>'+
					'<td id="collective-'+itemIdx+'">'+collectiveprice+'</td>'+
					'<td><img onclick="removeItem('+itemIdx+')" src="images/delete.png" style="cursor:pointer;" title="Delete item"/></td>');
					$('#new-item-form')[0].reset();
					itemIdx++;
				}
				else if(response.error == -2) {
					alert("only " + response.qty + " products are available");
				} else {
					alert('No such product exist');
				}
			}
		});
	});
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

function removeItem(index){

	var contents = $('td#collective-'+index).text();
	$('#item-'+index).remove();	
	totalPrice = totalPrice - parseFloat(contents).toFixed(2);
	$('#total-price').text(totalPrice);	
}

	
