var cart_list = [];
var store_selected = 0;
var total = 0;

function setStore(store_id)
{
	store_selected = store_id;
}
function addCart(prodid, prodname, quantity, price)
{
	var new_cart = new Object();
	new_cart.prodid = prodid;
	new_cart.prodname = prodname;
	new_cart.quantity = quantity;
	new_cart.price = price;
	cart_list.push(new_cart);
}

function editCart(prodid, quantity_edited)
{
	for c in cart_list
		if c.prodid = prodid
			c.quantity = quantity_edited

}

function deleteCart(prodid)
{
	for c in cart_list
		if c.prodid = prodid
			c.remove() // check
}

function calcTotal()
{
	for c in cart_list
		total = total + c.quantity*c.price
}