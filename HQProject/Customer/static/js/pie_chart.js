google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

window.onload = function() {
	drawChart();	
}	

function drawChart() {
$('#submit').click(function() {	
   var e = document.getElementById("cate");
   var strUser = e.options[e.selectedIndex].value;
	console.log(strUser);
	$.ajax({
		url: "http://127.0.0.1:8000/Website/revenue_pie",
		type: 'POST',
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		data:JSON.stringify({"region":strUser}),
		success: function (response) {
			var val = response.result;	
            console.log(val);
			 var array = []	
			 var header = []
			 header.push("storeid")
			 header.push("revenue");
			 array.push(header)
			 for (var a in val) {
				  var ar = []
				  ar.push(a);
				  ar.push(parseFloat(val[a]));
				  array.push(ar)
			  }

			console.log(array);
			   
			var data = google.visualization.arrayToDataTable(array);
				
			var options = {
			  title: 'Revenue per store this month'
			};

			var chart = new google.visualization.PieChart(document.getElementById('piechart'));
			chart.draw(data, options);	
			
		}
	});
});
}
