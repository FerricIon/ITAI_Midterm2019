<template lang="pug">
v-layout(row, wrap)
  v-flex.echart-container(xs4)
    v-chart(:options="genreDistribution", autoresize, @click="displaySingleTrend")
  v-flex.echart-container(xs8)
    v-chart(:options="keywordDistribution", autoresize)
  v-flex.echart-container(xs12)
    v-chart(:options="genreTrend", autoresize, ref="genreTrend")
</template>

<script>
import ECharts from 'vue-echarts'
import 'echarts'
import 'echarts-wordcloud'

export default {
  components: {
    'v-chart': ECharts
  },
  async asyncData({ $axios }) {
    const genres = new Map((await $axios.get('/api/genres')).data)
    const keywords = new Map((await $axios.get('/api/keywords')).data)
    const genreDistributionData = (await $axios.get('/api/genre-distribution')).data
    // eslint-disable-next-line
    console.log(genreDistributionData)
    const keywordDistributionData = (await $axios.get('/api/keyword-distribution')).data

    return {
      genreDistribution: {
        title: {
          text: 'Genre Distribution'
        },
        tooltip: {
          formatter: '{b}: {c}({d}%)'
        },
        series: [
          {
            name: 'Count',
            type: 'pie',
            radius: '40%',
            center: ['50%', '50%'],
            data: genreDistributionData.map(({ id, count }) => ({
              name: genres.get(id),
              value: count
            }))
          }
        ]
      },
      keywordDistribution: {
        baseOption: {
          timeline: {
            data: keywordDistributionData.map((o) => {
              return o.decade
            }),
            label: {
              formatter(value, index) {
                return value.toString()
              }
            },
            autoPlay: true,
            playInterval: 5000
          },
          title: {
            text: 'Keyword Distribution by 10 Years'
          },
          tooltip: {
            formatter: '{b}: {c}'
          },
          series: []
        },
        options: keywordDistributionData.map(({ distribution }) => {
          return {
            series: {
              title: '',
              type: 'wordCloud',
              shape: 'circle',
              width: '100%',
              height: '70%',
              data: distribution.map(({ id, count }) => {
                return {
                  name: keywords.get(id),
                  value: count
                }
              }),
              sizeRange: [10, 60],
              rotationStep: 30
            }
          }
        })
      },
      genreTrend: {
        title: {
          text: 'Genre Trend'
        },
        tooltip: {},
        legend: {
          show: true,
          type: 'scroll',
          animation: true,
          orient: 'vertical',
          top: '10%',
          right: 0,
          data: [...genres].map(([id, genre]) => genre).sort()
        },
        xAxis: {
          type: 'category',
          data: genreDistributionData[0].distribution.map(({ decade }) => decade),
          boundaryGap: false
        },
        yAxis: {
          type: 'value',
          scale: true
        },
        grid: {
          right: 200
        },
        dataZoom: {
          xAxisIndex: [0]
        },
        series: genreDistributionData.map(({ id, distribution }) => ({
          name: genres.get(id),
          type: 'line',
          data: distribution.map(({ decade, count }) => count),
          smooth: true
        }))
      }
    }
  },
  methods: {
    displaySingleTrend(param) {
      const chart = this.$refs.genreTrend
      chart.computedOptions.series.forEach(({ name }) => {
        chart.dispatchAction({
          type: name === param.name ? 'legendSelect' : 'legendUnSelect',
          name
        })
      })
    }
  }
}
</script>

<style scoped>
.echart-container {
  height: 50%;
}
.echarts {
  height: 100%;
  width: 100%;
}
</style>
