<template lang="pug">
v-app
  v-navigation-drawer(app, permanent, router)
    v-toolbar
      v-toolbar-title {{ title }}
    v-divider
    v-list(pt-0)
      v-list-tile(v-for="route in routes", :key="route.title", nuxt, :to="route.path")
        v-list-tile-action
          v-icon {{ route.icon }}
        v-list-tile-content
          v-list-tile-title {{ route.title }}
  v-content
    v-container(fluid, fill-height)
      nuxt
</template>

<script>
export default {
  data() {
    return {
      title: '',
      routes: [
        {
          icon: 'bar_chart',
          title: '数据可视化',
          path: '/visualization'
        },
        {
          icon: 'thumb_up',
          title: '推荐',
          path: '/recommendation'
        },
        {
          icon: 'star',
          title: '评分预测',
          path: '/rate'
        }
      ]
    }
  },
  mounted() {
    const pkg = require('../package')
    this.title = pkg.name
  }
}
</script>
