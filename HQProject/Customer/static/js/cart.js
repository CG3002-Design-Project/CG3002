var cart_list = {};
var store_selected = 0;
var totalPrice = 0;

window.onload = function() {
	 addToCart();
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
	var collectiveprice = parseFloat(val['selling_price'] * parseInt(val['quantity']));
	totalPrice = totalPrice + collectiveprice;
	$('#total-price').text(totalPrice);
	$('#item-table').append('<tr barcode="'+val['name']+'" class="items" id="item-'+itemIdx+'">'+
		'<td>'+val['name']+'</td>'+
		'<td>'+val['quantity']+'</td>'+
		'<td>'+val['selling_price']+'</td>'+
		'<td id="collective-'+itemIdx+'">'+collectiveprice+'</td>'+
	 '	<td><img onclick="removeItem('+itemIdx+')" src="/static/delete.png" style="cursor:pointer;" title="Delete item"/></td>');
	}
 }


function togglestyle(element){
	
	console.log("here");
	var class_v = $(element).attr('class');
	
	if(class_v == "on") {
		
			console.log("remove from cart")
			var currentRow = $(element).closest("tr");
			//do something with values in td's
			var productid = currentRow.find("td").eq(6).children("span").text();
			var quantity = currentRow.find('.quantity');
			quantity.value = 0;
			delete cart_list[productid];
			
			localStorage.setItem('cartObj', JSON.stringify(cart_list));
			var retrievedObject = localStorage.getItem('cartObj');
			console.log('retrievedObject after set: ', JSON.parse(retrievedObject));
			
			$(element).addClass('off').removeClass('on');
			$(element).val("Add to cart");
	
	} else if(class_v == "off") {
		
		//$('#tableClick').on('click', '#add_to_cart', function () {
			console.log("add to cart")
			var currentRow = $(element).closest("tr");
			//do something with values in td's
			var name = currentRow.find("td").eq(1).children("span").text();
			var selling_price = currentRow.find("td").eq(3).children("span").text();
			var batchid = currentRow.find("td").eq(4).children("span").text();
			var productid = currentRow.find("td").eq(5).children("span").text();
			var cost_price = currentRow.find("td").eq(6).children("span").text();
			var quantity = parseInt(currentRow.find('.quantity').val());
			console.log(quantity);
			if(isNaN(quantity)) {
				alert("quantity is empty");
			} 
			else 
			{
				var list = {}
				list['name']=name;
				list['selling_price']=selling_price;
				list['quantity']=quantity;
				list['batchid']=batchid;
				list['cost_price']=cost_price;
				
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