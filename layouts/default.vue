<template lang="pug">
v-app
  v-navigation-drawer(app, permanent, router)
    v-toolbar
      v-toolbar-title {{ title }}
    v-divider
    v-list(pt-0)
      v-list-tile(nuxt, to="/visualization")
        v-list-tile-action
          v-icon mdi-chart-bell-curve
        v-list-tile-content
          v-list-tile-title 可视化
      v-list-group(prepend-icon="mdi-thumb-up", v-model="recommendationActive", no-action, active-class="")
        template(slot="activator")
          v-list-tile
            v-list-tile-title 推荐
        v-list-tile(nuxt, to="/recommendation")
          v-list-tile-content
            v-list-tile-title 筛选
        v-list-tile(nuxt, to="/recommendation2")
          v-list-tile-content
            v-list-tile-title 协同过滤
      v-list-tile(nuxt, to="rate")
        v-list-tile-action
          v-icon mdi-star
        v-list-tile-content
          v-list-tile-title 评分预测
  v-content
    v-container(fluid, fill-height)
      nuxt
</template>

<script>
export default {
  data() {
    return {
      title: '',
      recommendationActive: false
    }
  },
  mounted() {
    const pkg = require('../package')
    this.title = pkg.name
  }
}
</script>
