window.onload = function() {
	initAddDisplay();
}

function validPriceDisplay(display_id, barcode,batchid, description){
	if (display_id.length == 0 || barcode.length == 0 || description.length == 0){
		alert('Invalid: Empty fields');
		return false;
	}
	if(barcode.trim().length != 8) {
		alert("barcode has to be 8 digits long");
		return false;
	}
	if(display_id.trim().length != 4) {
		alert("display has to be 4	 digits long");
		return false;
	}
	if (description.trim().length > 40)
	{
		alert('Description cannot exceed 40 characters!');
		return false;
	}
	return true;
}

function initAddDisplay(){
	$('#confirm-add-display').click(function(){
	    console.log("reached add button click method");
		var display_id = $('#inputId').val();
		var barcode = $('#inputBarcode').val();
		var batchid = $('#inputBatchid').val();
		var description = $('#inputDescription').val();
		if (validPriceDisplay(display_id, barcode,batchid,description))
			$.ajax({url: "http://127.0.0.1:8000/Inventory/check_display",
					type: 'POST',
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					data:JSON.stringify({
						"display_id":display_id,
						"barcode":barcode,
						"batchid" : batchid,
						"description" : description
					}),
					success: function (data) {
							  if(data.error == -1) {
								alert("No such product exists");
							  } else if (data.error == -2) {
								if (confirm('Are you sure you want to overwrite the display id?')) {
									console.log("over write display id");
									$.ajax({
									url: "http://127.0.0.1:8000/Inventory/setDisplayID",
									contentType: "application/json; charset=utf-8",
									dataType: "json",
									type: 'POST',
									data: JSON.stringify({
										"display_id":display_id,
										"barcode":barcode,
										"batchid" : batchid,
										"description":description
										}),
										success: function (response) {
											console.log("inside close button");
											$('#addNewDisplay').modal('hide');
										},
										error: function (response){
											alert(response.responseText);
										}										
								});
								}
								else {
										// Do nothing!
								}
							  } 
							  else if (data.error == 1) {
									$.ajax({
									url: "http://127.0.0.1:8000/Inventory/setDisplayID",
									contentType: "application/json; charset=utf-8",
									dataType: "json",
									type: 'POST',
									data: JSON.stringify({
										"display_id":display_id,
										"barcode":barcode,
										"batchid" : batchid,
										"description":description
										}),
										success: function (response) {
											console.log("inside close button");
											 $('#addNewDisplay').modal('hide');
										},
										error: function (response){
											alert(response.responseText);
										}
										});
							   }		
			     	}
		 });
    });

}

