var cart_list = {};
var store_selected = 0;
var totalPrice = 0;
var itemIdx = 0;

window.onload = function() {	
	 addToCart();
	 checkout();
}

function addToCart() {
	console.log("inside")
	var retrievedObject = localStorage.getItem('cartObj');
	console.log('retrievedObject: ', JSON.parse(retrievedObject));
	list = JSON.parse(retrievedObject)
	for(key in list) {
		console.log(key);
		val = list[key];
		console.log(val['name']);
		unitprice = val['selling_price']
		var collectiveprice = parseFloat(unitprice).toFixed(2) * parseInt(val['quantity']);
		totalPrice = totalPrice + collectiveprice;
		$('#total-price').text(totalPrice);
		$('#item-table').append('<tr class="items" id="item-'+itemIdx+'">'+
			'<td>'+val['name']+'</td>'+
			'<td>'+val['quantity']+'</td>'+
			'<td>'+val['selling_price']+'</td>'+
			'<td id="collective-'+itemIdx+'"  batchid="'+val['batchid']+'" productid="'+key+'" >'+collectiveprice+'</td>'+
		 '	<td><img onclick="removeItem('+itemIdx+')" src="/static/delete.png" style="cursor:pointer;" title="Delete item"/></td>');
		}
 }

 function removeItem(index){

	var contents = $('td#collective-'+index).text();
    var productid = $('td#collective-'+index).attr("productid");	
	var retrievedObject = localStorage.getItem('cartObj');
	cart_list = JSON.parse(retrievedObject)
	delete cart_list[productid]
	console.log("after delete",cart_list);
	
	localStorage.setItem('cartObj', JSON.stringify(cart_list));
	var retrievedObject = localStorage.getItem('cartObj');
	console.log('retrievedObject after set: ', JSON.parse(retrievedObject))
	$('#item-'+index).remove();	
	totalPrice = totalPrice - parseFloat(contents).toFixed(2);
	$('#total-price').text(totalPrice);	
	
}

 
 function checkout() {
		$('#confirm-checkout').click(function(){			
			var retrievedObject = localStorage.getItem('cartObj');
			cart_list = JSON.parse(retrievedObject)
			var a = "poo"
			$.ajax({
			url: 'http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Customer/add_eTransaction', 
			type: 'POST',
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify({'cart':cart_list}),
			success: function (response) {
				id = response.transaction_id
				bootbox.confirm("Order placed. Your transaction id is " + id , function(result) {	
						localStorage.setItem('cartObj', JSON.stringify(cart_list));
						var retrievedObject = localStorage.getItem('cartObj');
						cart_list = JSON.parse(retrievedObject);
						cart_list = {}
						localStorage.setItem('cartObj', JSON.stringify(cart_list));
						document.location.href="http://127.0.0.1:8000/Customer/inventory_list";
				});
				
			}
			});
		});
		$('#back').click(function(){
					console.log("back");
					document.location.href="http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Customer/inventory_list";	
		});
		
		$('#abort').click(function(){
				bootbox.confirm('Are you sure you want to abort the transaction?', function(result) {
						cart_list = {}
						console.log(cart_list);
						localStorage.setItem('cartObj', JSON.stringify(cart_list));
						var retrievedObject = localStorage.getItem('cartObj');
						console.log('retrievedObject after set: ', JSON.parse(retrievedObject))
						document.location.href="http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Customer/inventory_list";
				});
		});
 }

function togglestyle(element){
	localStorage.setItem('cartObj', JSON.stringify(cart_list));	
	console.log("here");
	var batchid = element.getAttribute("batchid")
	var productid = element.getAttribute("productid")
	var cost_price = element.getAttribute("cost_price")
	if($(element).hasClass("on")) {
		
			console.log("remove from cart")
			var currentRow = $(element).closest("tr");
			//do something with values in td's
			
			var quantity = currentRow.find('.quantity');
			quantity.value = 0;
			
			var retrievedObject = localStorage.getItem('cartObj');
			cart_list = JSON.parse(retrievedObject);
			delete cart_list[productid];
		    
			console.log("AFTER DELETE",cart_list);
			
			localStorage.setItem('cartObj', JSON.stringify(cart_list));
			var retrievedObject = localStorage.getItem('cartObj');
			console.log('retrievedObject after set: ', JSON.parse(retrievedObject));
			
			$(element).addClass('off').removeClass('on');
			$(element).val("Add to cart");
	
	} else if($(element).hasClass("off")) {
		
		//$('#tableClick').on('click', '#add_to_cart', function () {
			console.log("add to cart")
			var currentRow = $(element).closest("tr");
			//do something with values in td's
			var name = currentRow.find("td").eq(1).text();
			var selling_price = currentRow.find("td").eq(3).text();
			var quantity = parseInt(currentRow.find('.quantity').val());
			console.log(quantity);
			if(isNaN(quantity)) {
				bootbox.alert("Quantity is empty");
			} 
			else 
			{
				var list = {}
				list['name']=name;
				list['selling_price']=selling_price;
				list['quantity']=quantity;
				list['batchid']=batchid;
				list['cost_price']=cost_price;
				
				var retrievedObject = localStorage.getItem('cartObj');
				cart_list = JSON.parse(retrievedObject);
				
				cart_list[productid]=list;
				
				localStorage.setItem('cartObj', JSON.stringify(cart_list));
				var retrievedObject = localStorage.getItem('cartObj');
				console.log('retrievedObject after set: ', JSON.parse(retrievedObject));
				
				$(element).addClass('on').removeClass('off');
				$(element).val("added");
				
				}
				//});	
			}
	}	