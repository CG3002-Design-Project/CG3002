
var app = angular.module('myApp', []);
var GLOBALS = {};
GLOBALS.inventory = [];

function TransactionCtrl($scope, $http) {
	console.log("controller initialised");
	$scope.inventory = GLOBALS.inventory;
    $scope.loadTransaction = function(barcode, quantity) {
		console.log(typeof barcode);
		if(barcode.toString().length != 8 || !isNumber(parseInt(barcode))) {
				alert("barcode has to be a valid 8 digit number!!");
		}
		else if(!isNumber(parseInt(quantity)) || parseInt(quantity) <= 0 ) {
				alert("quantity should be greater than 0");
		} 
		else{
		
		$http({method:'POST', 
			  url: 'http://127.0.0.1:8000/Inventory/returnPrice', 
			  data: {'barcode' : barcode, 'qty': quantity}}).success(function(data){	
			  GLOBALS.inventory[GLOBALS.inventory.length] = data;	  
		})
		.error(function( data, status, header,config ) {
			var err = status + ", " + data;
			console.log( "Request Failed: " + err );
        });
		
		}
	}
	
}


function isNumber(n){
    return typeof n == 'number' && !isNaN(n) && isFinite(n);
 }
