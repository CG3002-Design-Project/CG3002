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
		url: "http://127.0.0.1:8000/Website/price_topTen",
		type: 'POST',
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		data:JSON.stringify({"storeid":strUser}),
		success: function (response) {
			var val = response.result;	
            console.log(val);
			 var array = []	
			 var header = []
			 header.push('prodid')
			 header.push('revenue');
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
			  title: 'Top 10 Products',
			   vAxis: {title: 'Product Name',  titleTextStyle: {color: 'red'}}
			};

			var chart = new google.visualization.BarChart(document.getElementById('bar_chart'));
			chart.draw(data, options);	
			
		}
	});
});
}
