$(document).ready(function () {

	$("#predictButton").click(function () {
		var popup = document.getElementById("popup10");
		popup.classList.toggle("show");
		$("#predictButton").prop("disabled", true);
		$.ajax({
			url: '/predict',
			type: 'POST',
			data: {
				date: date,
				prediction_type: 0
			},
			success: function (response) {
				updatePlotWithPrediction(response)
				update10minFields(response)
			},
			complete: function () {
				popup.classList.toggle("show");
				$("#predictButton").prop("disabled", false);
			}
		});
	});

	$("#predict1Button").click(function () {
		var popup = document.getElementById("popup1");
		popup.classList.toggle("show");
		$("#predict1Button").prop("disabled", true);
		$.ajax({
			url: '/predict',
			type: 'POST',
			data: {
				date: date,
				prediction_type: 1
			},
			success: function (response) {
				update1minFields(response)
			},
			complete: function () {
				popup.classList.toggle("show");
				$("#predict1Button").prop("disabled", false);
			}
		});
	});

	$("#predict60Button").click(function () {
		var popup = document.getElementById("popup60");
		popup.classList.toggle("show");
		$("#predict60Button").prop("disabled", true);
		$.ajax({
			url: '/predict',
			type: 'POST',
			data: {
				date: date,
				prediction_type: 2
			},
			success: function (response) {
				update60minFields(response)
			},
			complete: function () {
				popup.classList.toggle("show");
				$("#predict60Button").prop("disabled", false);
			}
		});
	});

	function update10minFields(response) {
		$("#predictedPrice10min").html(response[response.length - 1])
		console.log(response[response.length - 11])
		if (response[response.length - 10] < response[response.length - 1])
			direction = "UP"
		else
			direction = "DOWN"
		$("#predictedDirection10min").html(direction)
	}
	function update1minFields(response) {
		$("#predictedPrice1min").html(response)
		if (yprices[yprices.length - 1] < response[0])
			direction = "UP"
		else
			direction = "DOWN"
		$("#predictedDirection1min").html(direction)
	}
	function update60minFields(response) {
		if (response[response.length - 1] < response[0])
			direction = "DOWN"
		else
			direction = "UP"
		$("#predictedDirection60min").html(direction)
	}
	function updatePlotWithPrediction(newData) {
		var newDataset = {
			label: 'Prediction: AAPL',
			data: newData.slice(Math.max(newData.length - number_of_shown_prices, 0)),
			borderColor: 'rgba(255, 99, 132, 1)',
			backgroundColor: 'rgba(255, 99, 132, 0.2)'
		};
		chart.data.datasets.push(newDataset)
		chart.update();
	}
});