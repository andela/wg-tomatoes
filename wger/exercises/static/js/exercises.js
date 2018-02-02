/*
 This file is part of wger Workout Manager.

 wger Workout Manager is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 wger Workout Manager is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 */

/*
 wger exercise functions
 */

'use strict';

/*
 Highlight a muscle in the overview
 */
function wgerHighlightMuscle(element) {
  var $muscle;
  var muscleId;
  var isFront;
  var divId;
  divId = $(element).data('target');
  isFront = ($(element).data('isFront') === 'True')
    ? 'front'
    : 'back';
  muscleId = divId.match(/\d+/);

  // Reset all other highlighted muscles
  $muscle = $('.muscle');
  $muscle.removeClass('muscle-active');
  $muscle.addClass('muscle-inactive');

  // Highlight the current one
  $(element).removeClass('muscle-inactive');
  $(element).addClass('muscle-active');

  // Set the corresponding background
  $('#muscle-system').css('background-image', 'url(/static/images/muscles/main/muscle-' + muscleId + '.svg),url(/static/images/muscles/muscular_system_' + isFront + '.svg)');

  // Show the corresponding exercises
  $('.exercise-list').hide();
  $('#' + divId).show();
}

/*
 D3js functions
 */

function wgerDrawWeightLogChart(data, divId) {
  var chartData;
  var legend;
  var minValues;
  var i;
  if (data.length) {
    legend = [];
    minValues = [];
    chartData = [];
    for (i = 0; i < data.length; i++) {
      chartData[i] = MG
        .convert
        .date(data[i], 'date');
      // Read the possible repetitions for the chart legend
      legend[i] = data[i][0].reps;

      // Read the minimum values for each repetition
      minValues[i] = d3.min(data[i], function (repetitionData) {
        return repetitionData.weight;
      });
    }

    MG.data_graphic({
      data: chartData,
      y_accessor: 'weight',
      min_y: d3.min(minValues),
      aggregate_rollover: true,
      full_width: true,
      top: 10,
      left: 30,
      right: 10,
      height: 200,
      legend: legend,
      target: '#svg-' + divId,
      colors: [
        '#204a87',
        '#4e9a06',
        '#ce5c00',
        '#5c3566',
        '#2e3436',
        '8f5902',
        '#a40000'
      ]
    });
  }
}

/**
 * @param {array} data User data to use when drawing bar graph
 * @param {array} otherUserData Other user data to use during comparison
 * @param {string} divId Id of the html element to use when drawing the draph
 * @param {string} otherUser The username of the other user
 */
function wgerDrawBarGraph(data, otherUserData, divId, otherUser) {
  //get the element defined by this div
  var context = document.getElementById('svg-' + divId);

  //grab logged in user data
  var listOfChartData = [];
  var chartData = getChartData(data);
  listOfChartData.push(chartData);

  // check if user data of the other user is included
  if (otherUserData) {
    var otherUserBarGraphData = [];
    var otherChartData = getChartData(otherUserData);
    otherUserBarGraphData.push(otherChartData);

    //generate data for both users to draw the bar graph
    data = {
      labels: listOfChartData[0]
        .dates
        .slice(0, 6),
      datasets: [
        getSingleDataset("My weights",'#76ff03','#64dd17', listOfChartData, "weight"), 
        getSingleDataset("My reps",'#b2ff59','#76ff03', listOfChartData, "reps"),
        getSingleDataset(otherUser + "'s weights",'#ff9100','#ff6d00', otherUserBarGraphData, "weight"),
        getSingleDataset(otherUser + "'s reps",'#ffab40','#ff9100', otherUserBarGraphData, "reps"),
      ]
    };

    //draw the bar graph
    drawBarGraph(context, data);
  } else {
    //get userdata to draw the bar graph
    data = {
      labels: listOfChartData[0]
        .dates
        .slice(0, 6),
      datasets: [
        getSingleDataset("My weights",'#76ff03','#64dd17', listOfChartData,'weight')
        ,
        getSingleDataset("My reps", "#b2ff59", "#76ff03",listOfChartData,"reps"),
      ]
    }
    //draw the bar graph
    drawBarGraph(context, data);
  }
}

/**
 * Uses Charts.js to draw a bar graph
 * @param {element} context The html canvas to update
 * @param {data} data The data to use when plotting the bar graph 
 */
function drawBarGraph(context, data) {
  var wgerBarGraph = new Chart(context, {
    type: 'bar',
    data: data,
    options: {}
  });
}

/**
 * Generates an object containing data ready to use to draw the graphs
 * @param {array} data An array of objects containing data to usse when plotting graph
 */
function getChartData(data) {
  var newUserData = {
    dates: [],
    weight: [],
    reps: []
  };

  data.forEach((element) => {
    element
      .slice(0, 6)
      .forEach((item) => {
        newUserData
          .dates
          .push(item.date);
        newUserData
          .weight
          .push(item.weight);
        newUserData
          .reps
          .push(item.reps);
      });
  })

  return newUserData;
}

/**
 * Generates a dataset to be plotted on a graph
 * @param {string} label The label of the abr
 * @param {string} bgColor The color of the bar
 * @param {string} borderColor The outline of the bar graph
 * @param {array} data Array containing data to use when plotting
 * @param {*} type The type of data to generate. Can be 'reps' or 'weight'
 */
function getSingleDataset(label, bgColor, borderColor, data, type) {
  return {
    label: label,
    backgroundColor: bgColor,
    borderColor: borderColor,
    data: type === 'weight'
      ? data[0]
        .weight
        .slice(0, 6)
      : data[0]
        .reps
        .slice(0, 6)
  }
}
