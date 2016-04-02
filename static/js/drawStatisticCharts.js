/**
 * Created by daria on 02.04.16.
 */

var colrs = ['#40C4FF','#01579B','#B2FF59','#76FF03','#64DD17','#B3E5FC','#81D4FA','#4FC3F7','#039BE5','#0288D1','#0277BD',
               '#01579B','#DCEDC8','#C5E1A5','#AED581','#9CCC65','#8BC34A','#7CB342']
var chartWidht = 700;
var chartHeight = 350;

function drawChartDay() {
    var data = google.visualization.arrayToDataTable([
        ['', '', { role: 'annotation' }],
        ['День 1', 65, 'День 1'],
        ['День 2', 98, 'День 2'],
        ['День 3', 102, 'День 3'],
        ['День 4', 102, 'День 4']
    ]);
    var options = {
        annotation: {},
        fontSize: 16,
        height: chartHeight,
        width: chartWidht,
        tooltip: {textStyle: {color: '#42A5F5'}, showColorCode: true},
        legend: {position: 'none'},
        colors: colrs,
        bar: {groupWidth: '75%'},
        axes: {x: {0: {side: 'top'}}}

    };
    var chartDay = new google.charts.Bar(document.getElementById('chart_onDay'));
    chartDay.draw(data, google.charts.Bar.convertOptions(options));
}

function drawChartSex() {
    var data = google.visualization.arrayToDataTable([
      ['', '', { role: 'annotation' }],
      ['М', 123, 'М'],
      ['Ж', 91, 'Ж']
    ]);
    var options = {
        fontSize: 16,
        height: chartHeight,
        width: chartWidht,
        tooltip: {textStyle: {color: '#42A5F5'}, showColorCode: true},
        legend: {position: 'none'},
        colors: colrs,
        bar: {groupWidth: "75%"},
        axes: {x: {0: {side: 'top'}}}
    };
    var chartSex = new google.charts.Bar(document.getElementById('chart_onSex'));
    chartSex.draw(data, google.charts.Bar.convertOptions(options));
}

function drawChartQual() {
    var data = google.visualization.arrayToDataTable([
        ['', '', { role: 'annotation' }],
        ['I', 95, 'I'],
        ['II', 56, 'II'],
        ['III', 31, 'III'],
        ['б/р', 25, 'б/р'],
    ]);
    var options = {
        fontSize: 16,
        height: chartHeight,
        width: chartWidht,
        tooltip: {textStyle: {color: '#42A5F5'}, showColorCode: true},
        legend: {position: 'none'},
        colors: colrs,
        bar: {groupWidth: '75%'},
        axes: {x: {0: {side: 'top'}}}
    };
    var chartQual = new google.charts.Bar(document.getElementById('chart_onQual'));
    chartQual.draw(data, google.charts.Bar.convertOptions(options));
}

google.load("visualization", "1", {packages:['corechart']});

// Call function to draw chart
$( document ).ready(function() {
    google.charts.load('current', {packages: [ 'bar']});
    google.charts.setOnLoadCallback(drawChartDay);
    google.charts.setOnLoadCallback(drawChartSex);
    google.charts.setOnLoadCallback(drawChartQual);
});