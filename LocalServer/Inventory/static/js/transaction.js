
var app = angular.module('myApp', []);
var GLOBALS = {};
GLOBALS.inventory = [];

function TransactionCtrl($scope, $http) {
	console.log("controller initialised");
	$scope.inventory = GLOBALS.inventory;
    
	$scope.loadTransaction = function(barcode, batchid, quantity) {
		if(barcode.length != 8 || !isNumber(parseInt(barcode))) {
				alert("barcode has to be a valid 8 digit number!!");
		}
		else if(batchid.length !=4 || !isNumber(parseInt(batchid))) {
				alert("Batch id has to be a valid 5 digit number!!"); 
		}
		else if(!isNumber(parseInt(quantity)) || parseInt(quantity) <= 0 ) {
				alert("quantity should be greater than 0");
		} 
		else{
		
			  $http({method:'POST', 
			  url: 'http://127.0.0.1:8000/Inventory/returnPrice', 
			  data: {'barcode' : barcode,'batchid': batchid, 'qty': quantity}}).success(function(data){	
			  console.log(data.error);
			  if(data.error == -1) {
				alert("No such product exists");
			  } else if (data.error == -2) {
				alert("only " + data.qty + " products are available");
			  } else {
					GLOBALS.inventory[GLOBALS.inventory.length] = data;	 		
			  }
		})
		.error(function( data, status, header,config ) {
			var err = status + ", " + data;
			console.log( "Request Failed: " + err );
        });
		
		}
	}
	
	$scope.cancelTransaction = function() {
		if (confirm('Are you sure you want to cancel the transaction?')) {
			console.log("add qty back to products");
			$http({method:'POST', 
				   url: 'http://127.0.0.1:8000/Inventory/addQuantity', 
				   data: GLOBALS.inventory}).success(function(data){
						console.log("Quantity added back");
						$scope.inventory.splice(0, 1);
				   });	
		} else {
				// Do nothing!
		}
	}
	
	$scope.checkOut = function() {
		if (confirm('Are you done shopping?')) {
				console.log("Saving transaction");
				$http({method:'POST', 
					url: 'http://127.0.0.1:8000/Inventory/saveTransaction', 
					data: GLOBALS.inventory}).success(function(data){
						console.log("Transaction added");
						$scope.inventory.splice(0, 1);
				   });	
		} else {
				// Do nothing!
		}
	}
}


function isNumber(n){
    return typeof n == 'number' && !isNaN(n) && isFinite(n);
 }

