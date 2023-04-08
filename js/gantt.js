google.charts.load('current', { 'packages': ['gantt'] });
google.charts.setOnLoadCallback(drawChart);

function daysToMilliseconds(days) {
    return days * 24 * 60 * 60 * 1000;
}

function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Task ID');
    data.addColumn('string', 'Task Name');
    data.addColumn('date', 'Start Date');
    data.addColumn('date', 'End Date');
    data.addColumn('number', 'Duration');
    data.addColumn('number', 'Percent Complete');
    data.addColumn('string', 'Dependencies');
    data.addRows([
        ['RA1', 'First Round of Requirement Analysis',
            new Date(2023, 2, 19), new Date(2023, 2, 23), null, 100, null],
        ['RA2', 'Second Round of Requirement Analysis',
            new Date(2023, 2, 23), new Date(2023, 2, 30), null, 90, null],
        ['SD1', 'First Round of Software Design',
            new Date(2023, 2, 31), new Date(2023, 3, 6), null, 80, 'RA1,RA2'],
        ['CODE1', 'First Round of Coding',
            new Date(2023, 3, 7), new Date(2023, 3, 16), null, 0, 'SD1'],
        ['TEST1', 'First Round of Testing',
            new Date(2023, 3, 14), new Date(2023, 3, 20), null, 0, 'SD1,CODE1'],
        ['TEST2', 'System Integration Testing',
            new Date(2023, 3, 21), new Date(2023, 3, 27), null, 0, 'CODE1,TEST1'],
    ]);

    var options = {
            height: 275
        };
    var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

    chart.draw(data, options);
}