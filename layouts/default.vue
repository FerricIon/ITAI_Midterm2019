<template lang="pug">
v-app
  v-navigation-drawer(v-model="drawer", :clipped="$vuetify.breakpoint.lgAndUp", app, router)
    v-list
      v-list-tile(nuxt, to="/visualization")
        v-list-tile-action
          v-icon mdi-chart-bell-curve
        v-list-tile-content
          v-list-tile-title Visualization
      v-list-group(prepend-icon="mdi-thumb-up", v-model="recommendationActive", no-action, active-class="")
        template(slot="activator")
          v-list-tile
            v-list-tile-title Recommendation
        v-list-tile(nuxt, to="/recommendation")
          v-list-tile-content
            v-list-tile-title Simple Filtering
        v-list-tile(nuxt, to="/recommendation2")
          v-list-tile-content
            v-list-tile-title Collaborative Filtering
      v-list-tile(nuxt, to="rate")
        v-list-tile-action
          v-icon mdi-star
        v-list-tile-content
          v-list-tile-title Rate Forecast
  v-toolbar(:clipped-left="$vuetify.breakpoint.lgAndUp", color="blue darken-3", dark, app, fixed)
    v-toolbar-title.ml-0.pl-3(style="width: 300px")
      v-toolbar-side-icon(@click.stop="drawer = !drawer")
      span {{ title }}
  v-content
    v-container(fluid, fill-height)
      nuxt
</template>

<script>
export default {
  data() {
    return {
      drawer: this.$vuetify.breakpoint.lgAndUp,
      title: '',
      showInfo: false,
      recommendationActive: false
    }
  },
  mounted() {
    const pkg = require('../package')
    this.title = pkg.name
  }
}
</script>

<style scoped>
.no-underscore {
  color: white;
  text-decoration: none;
}
</style>
