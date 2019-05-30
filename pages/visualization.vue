<template lang="pug">
v-layout(:row="$vuetify.breakpoint.lgAndUp", :column="$vuetify.breakpoint.mdAndDown", wrap)
  v-flex(lg4, :class="echartBoxClass")
    v-chart(:options="genreDistribution", autoresize, @click="displaySingleTrend", ref="genreDistribution")
  v-flex(lg8, :class="echartBoxClass")
    v-chart(:options="keywordDistribution", autoresize, ref="keywordDistribution")
  v-flex(lg12, :class="echartBoxClass")
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
  data() {
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
            data: []
          }
        ]
      },
      keywordDistribution: {
        baseOption: {
          timeline: {
            data: [],
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
        options: []
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
          data: []
        },
        xAxis: {
          type: 'category',
          data: [],
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
        series: []
      }
    }
  },
  computed: {
    echartBoxClass() {
      return [this.$vuetify.breakpoint.lgAndUp ? 'echart-box-lg' : 'echar-box-md']
    }
  },
  mounted() {
    this.$refs.genreDistribution.showLoading()
    this.$refs.keywordDistribution.showLoading()
    this.$refs.genreTrend.showLoading()
    this.$axios.$get('/api/genres').then((data) => {
      const genres = new Map(data.map(({ id, genre }) => ([id, genre])))
      this.genreTrend.legend.data = [...genres].map(([id, genre]) => genre).sort()
      this.$axios.$get('/api/genre-distribution').then((data) => {
        this.genreDistribution.series[0].data = data.map(({ id, count }) => ({
          name: genres.get(id),
          value: count
        }))
        this.$refs.genreDistribution.hideLoading()
        this.genreTrend.xAxis.data = data[0].distribution.map(({ decade }) => decade)
        this.genreTrend.series = data.map(({ id, distribution }) => ({
          name: genres.get(id),
          type: 'line',
          data: distribution.map(({ decade, count }) => count),
          smooth: true
        }))
        this.$refs.genreTrend.hideLoading()
      })
    })
    this.$axios.$get('/api/keywords').then((data) => {
      const keywords = new Map(data.map(({ id, keyword }) => ([id, keyword])))
      this.$axios.$get('/api/keyword-distribution').then((data) => {
        this.keywordDistribution.baseOption.timeline.data = data.map(({ decade }) => ({
          value: parseInt(decade),
          tooltip: false
        }))
        this.keywordDistribution.options = data.map(({ distribution }) => {
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
              rotationStep: 10,
              rotationRange: [-30, 30]
            }
          }
        })
        this.$refs.keywordDistribution.hideLoading()
      })
    })
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
.echart-box-lg {
  height: 50%;
}
.echar-box-md {
  height: 600px;
}
.echarts {
  height: 100%;
  width: 100%;
}
</style>
