

document.addEventListener('DOMContentLoaded', function () {

  const endpoint = '/api/fetch-data';

  fetch(endpoint)
    .then(response => {
      if (!response.ok) {
        throw new Error('Netowrk response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('issue with fetch operation', error);
    });
});



/*--
//Current Packets Count line chart
// This graph shows the overall count of all packets
//I need to change this to show packets at a specific time stamp as malicious or non-malicious
var pktCountChartDom = document.getElementById('packetCount');
var pktCountChart = echarts.init(pktCountChartDom);
var option;
//^This is where graphic is assigned to DOM element

// Function to fetch packet count from API
function fetchPacketCount() {
  return fetch('/api/fetch-pkt-count')
  .then(response => response.json())
  .then(data => data.pkt_count)  
  .catch(error => {
    console.error('Error fetching packet count:', error);
    return 0;  // Return 0 if there was an error
  });
}

// Function to generate new data with timestamp and packet count from API
function pktCount() {
  now = new Date(+now + oneSec);  // Increment time by one second
  return fetchPacketCount().then(packetCount => {
    return {
      name: now.toString(),  // Timestamp as name
      value: [
        now.getTime(),  // Use the timestamp in milliseconds for time axis
        packetCount  // Packet count for Y-axis
      ]
    };
  });
}

// Initialize chart data, current time, and value
let data = [];
let now = new Date();
let oneSec = 1000;  // One second in milliseconds

// Generate initial data
(async function initializeData() {
  for (var i = 0; i < 100; i++) {  // Initialize with 100 points
  let dataPoint = await pktCount();
  data.push(dataPoint);
  }
})();

// Define chart options with hidden xAxis labels and custom tooltip
option = {
  
tooltip: {
  trigger: 'axis',
  formatter: function (params) {
    params = params[0];
    var date = new Date(params.value[0]);  // Convert timestamp to date
    var hours = date.getHours().toString().padStart(2, '0');  // Format hours
    var minutes = date.getMinutes().toString().padStart(2, '0');  // Format minutes
    var seconds = date.getSeconds().toString().padStart(2, '0');  // Format seconds
    var time = hours + ':' + minutes + ':' + seconds;
    
    return `Time: ${time} <br/> Packet Count: ${params.value[1]}`;  // Show time and packet count
  },
  axisPointer: {
    animation: false
  }
},
xAxis: {
  type: 'time',
  splitLine: {
    show: false
  },
  axisLabel: {
    show: false  // Hide x-axis labels
  }
},
yAxis: {
  type: 'value',
  boundaryGap: [0, '100%'],
  splitLine: {
    show: false
  }
},
series: [
  {
    name: 'Packet Count',
    type: 'line',
    showSymbol: false,
    data: data
  }
]
};

// Update chart every 1000 milliseconds (1 second)
setInterval(async function () {
  for (var i = 0; i < 5; i++) {  // Shift out old data and add new data
  data.shift();  // Remove oldest data point
  let newData = await pktCount();
  data.push(newData);  // Add new data from API
}

// Update chart with the new data
pktCountChart.setOption({
  series: [
    {
      data: data
    }
  ]
});
}, 1000);  // Update interval is 1000 milliseconds (1 second)

option && pktCountChart.setOption(option);

----------------------------------------------*/
/*------------------------------------------------------------*/




//total Attacks Donut Chart
document.addEventListener("DOMContentLoaded", () => {
  new Chart(document.querySelector('#totalAttacks'), {
    type: 'doughnut',
    data: {
      labels: [
        'Severity level 1',
        '2', '3', '4'
      ],
      datasets: [{
        label: 'Total Attacks',
        data: [300, 50, 100, 200],
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)',
          'rgb(255, 0, 0)'
        ],
        hoverOffset: 4
      }]
    }
  });
});

//all devices table
document.addEventListener('DOMContentLoaded', function () { //is page loaded?

  const endpoint = '/api/fetch-devices';
  fetch(endpoint) //get data for all devices
    .then(response => {
      if (!response.ok) {
        throw new Error('Netowrk response was not ok');
      }
      return response.json();
    })
    .then(data => { //response is ok 
      
      //data that will be directly inserted into table
      let devices = [];
      
            //loop through fetch response and insert into table data
            for (const [key, device] of Object.entries(data.devices)) {
              let deviceObj = {};
              deviceObj.id = `${device.id}`;
              deviceObj.name = `${device.name}`;
              deviceObj.OUI = `${device.OUI}`;
              deviceObj.comp_id = `${device.comp_id}`;
              deviceObj.group = `${device.group}`;
              deviceObj.mal = `${device.mal}`;
              devices.push(deviceObj);
            }
            console.log(devices);
      
      const deviceTable = document.querySelector('#deviceTable');

      const hotDT = new Handsontable(deviceTable, {
        data: devices,
        columns: [
          {
            title: 'id',
            type: 'numeric',
            data: 'id',
          },
          {
            title: 'name',
            type: 'text',
            data: 'name',
          },
          {
            title: 'OUI',
            type: 'text',
            data: 'OUI',
          },
          {
            title: 'comp_id',
            type: 'text',
            data: 'comp_id',
          },
          {
            title: 'group',
            type: 'text',
            data: 'group',
          },
          {
            title: 'malicious?',
            type: 'text',
            data: 'mal',
          },
        ],
        // enable filtering
        filters: true,
        // enable the column menu
        dropdownMenu: ['filter_by_condition', 'filter_by_value', 'filter_action_bar'],
        height: 'auto',
        autoWrapRow: true,
        autoWrapCol: true,
        readOnly: true,
        afterFilter: function(){
          console.log(hotDT.countRows()) // have this appear on page as filter results
        },
        licenseKey: 'non-commercial-and-evaluation',
      });

    })
})