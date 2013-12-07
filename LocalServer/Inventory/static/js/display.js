window.onload = function() {
	initAddDisplay();
}

function validPriceDisplay(display_id, barcode,batchid, description){
	if (display_id.length == 0 || barcode.length == 0 || description.length == 0){
		bootbox.alert('Invalid: Empty fields');
		return false;
	}
	if(barcode.trim().length != 8) {
		bootbox.alert("barcode has to be 8 digits long");
		return false;
	}
	if(display_id.trim().length != 6) {
		bootbox.alert("display has to be 6	 digits long");
		return false;
	}
	if (description.trim().length > 40)
	{
		bootbox.alert('Description cannot exceed 40 characters!');
		return false;
	}
	return true;
}


function edit_display(display_id,barcode,batchid,description) {
		if (validPriceDisplay(display_id, barcode,batchid,description))
			console.log("valid");
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
								bootbox.alert("No such product exists");
							  } else if (data.error == -2) {
								bootbox.confirm('Are you sure you want to overwrite the display id?', function(result) {
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
											console.log(description);
											if(description == 'edit') {
												console.log("ajax");
												document.location.href="http://127.0.0.1:8000/Inventory/display";
											}		
											else {		
												$('#addNewDisplay').modal('hide');
												location.reload();
											}	
										},
										error: function (response){
											bootbox.alert(response.responseText);
										}										
								});
								});
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
											console.log(description);
											if(description == 'edit') {
												console.log("ajax");
												document.location.href="http://127.0.0.1:8000/Inventory/display";
											}		
											else {		
												$('#addNewDisplay').modal('hide');
												location.reload();
											}
										},
										error: function (response){
											bootbox.alert(response.responseText);
										}
										});
							   }		
			     	}
		 });

}

function initAddDisplay(){
	$('#confirm-add-display').click(function(){
	    console.log("reached add button click method");
		var display_id = $('#inputId').val();
		var barcode = $('#inputBarcode').val();
		var batchid = $('#inputBatchid').val();
		var description = $('#inputDescription').val();
		edit_display(display_id,barcode,batchid,description);
    });
	$('#editDisplay').click(function(){
	    console.log("YAAYNESS");
		var display_id = $('#display_id').val();
		console.log(display_id);
		var barcode = $('#product_id').val();
		console.log(barcode);
		var batchid = $('#batch_id').val();
		console.log(batchid);
		var description = "edit" 
		edit_display(display_id,barcode,batchid,description);
    });
	$('#refreshDisplay').click(function(){
	    console.log("refresh display is clicked");
		$.ajax({
				url: "http://127.0.0.1:8000/Inventory/write_to_display",
				success: function (response) {
					bootbox.alert("LCD reset successfully");
				}
				});
				
    });
	$('#cancel').click(function(){
	    console.log("refresh display is clicked");
		document.location.href="http://127.0.0.1:8000/Inventory/display";
    });
}

