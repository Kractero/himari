function generateDateRange(startDate) {
  const dates = []
  const currentDate = new Date()
  let current = new Date(startDate)

  while (
    current < currentDate ||
    (current.getFullYear() === currentDate.getFullYear() &&
      current.getMonth() === currentDate.getMonth() &&
      current.getDate() === currentDate.getDate())
  ) {
    const year = current.getFullYear()
    const month = String(current.getMonth() + 1).padStart(2, '0')
    const day = String(current.getDate()).padStart(2, '0')
    dates.push(`${year}-${month}-${day}`)
    current.setDate(current.getDate() + 1)
  }

  return dates
}

const startDate = '2023-10-05'
const dateRange = generateDateRange(startDate)

let chart
function initChart() {
  chart = Highcharts.chart('container', {
    title: { text: 'Nation Cards Data' },
    xAxis: { categories: dateRange, tickInterval: 30 },
    series: [],
    plotOptions: {
      line: {
        marker: {
          enabled: false,
        },
        connectNulls: true,
        lineWidth: 2,
      },
    },
  })
}

async function loadData() {
  const data = []
  for (const date of dateRange) {
    try {
      const response = await fetch(`/data/${date}.json`)
      const jsonData = await response.json()
      data.push(jsonData)
    } catch (error) {
      data.push([])
      //   console.error(`Failed to load data for ${date}:`, error)
    }
  }

  return data
}

async function updateChart() {
  const selectedMetric = document.getElementById('metricDropdown').value
  const nationInput = document.getElementById('nationInput').value.trim()
  const selectedNations = nationInput
    .split(',')
    .map(n => n.trim())
    .filter(n => n.length > 0)

  if (selectedNations.length === 0) {
    alert('Please enter at least one nation.')
    return
  }

  while (chart.series.length) {
    chart.series[0].remove(true)
  }

  const data = await loadData()

  selectedNations.forEach(nation => {
    let firstValidDateIndex = -1

    const seriesData = data.map((entryArray, index) => {
      const nationData = entryArray.find(n => n.Nation === nation)
      if (nationData && nationData[selectedMetric] !== null) {
        if (firstValidDateIndex === -1) {
          firstValidDateIndex = index
        }
        return nationData[selectedMetric]
      }
      return null
    })

    if (firstValidDateIndex !== -1) {
      if (selectedNations.length === 0) {
        const filteredSeriesData = seriesData.slice(firstValidDateIndex)
        const filteredDateRange = dateRange.slice(firstValidDateIndex)

        chart.addSeries({
          name: nation,
          data: filteredSeriesData,
        })

        chart.xAxis[0].setCategories(filteredDateRange)
      } else {
        chart.addSeries({
          name: nation,
          data: seriesData,
        })
      }
    } else {
      console.warn(`Nation "${nation}" not found in the data or has no valid data for the selected metric.`)
    }
  })
}

initChart()
