var chart;
var yprices;
var xlabels;

var number_predictions = 10

var number_of_shown_prices = 250;

$(document).ready(function () {

    var ctx = document.getElementById('chart').getContext('2d');

    //Parse current prices
    yprices = parse_prices_y(current_prices)

    //Parse datetimes from prices
    xlabels = parse_dates_x(datetimes_prices)

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xlabels,
            datasets: [{
                label: 'Stock Price: AAPL',
                data: yprices,
                fill: true,
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                borderColor: '#ffffff',
                borderWidth: 1
            }]
        }, options: {
            legend: {
                labels: {
                    fontColor: "#A8A7A7",
                    fontSize: 14
                }
            },
            scales: {
                xAxes: [{
                    ticks: {
                        maxRotation: 50,
                        minRotation: 30,
                        padding: 20,
                        autoSkip: false,
                        fontSize: 14,
                        fontColor: "#A8A7A7"
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontSize: 14,
                        fontColor: "#A8A7A7"
                    }
                }]
            }
        }
    });
});


function parse_prices_y(prices) {
    prices = prices.replace('[', '')
    prices = prices.replace(']', '')
    prices = prices.split(",").map(Number)
    return prices.slice(-number_of_shown_prices + number_predictions)
}

function parse_dates_x(dates) {
    dates = dates.split(":00,");
    datetimes_prices_light = []
    counter_for_labels = 0
    for (var i = dates.length - number_of_shown_prices; i < dates.length; i++) {
        if (i % 5 == 0 && counter_for_labels < yprices.length) {
            myDate = new Date(dates[i + number_predictions])
            minutes = myDate.getMinutes()
            hours = myDate.getHours()
            if (minutes < 10)
                minutes = "0" + minutes
            if (hours < 10)
                hours = "0" + hours
            datetimes_prices_light.push(hours + ":" + minutes)
        }
        else
            datetimes_prices_light.push("")
        counter_for_labels += 1
    }
    return datetimes_prices_light
}