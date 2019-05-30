<template lang="pug">
v-layout(:row="$vuetify.breakpoint.lgAndUp", :column="$vuetify.breakpoint.mdAndDown", wrap)
  v-flex(lg4)
    v-autocomplete(
      v-model="userMovies.model",
      :loading="userMovies.loading",
      :search-input.sync="userMovies.search",
      :items="userMovies.items",
      label="Film Name",
      multiple,
      cache-items
    )
    v-container(v-if="$vuetify.breakpoint.lgAndUp", grid-list-sm, fluid, fill-height)
      v-layout(row, wrap)
        v-flex(xs12, sm6, md4, lg6 v-for="(movie, ind) in userMovies.model", :key="movie")
          v-movie(:movie-id="movie", closable, @close="userMovies.model.splice(ind, 1)")
  v-flex(lg8)
    v-container(grid-list-md, fluid, fill-height)
      v-layout(align-center, justify-center, fill-height, wrap)
        v-progress-circular(v-if="loadingResult", indeterminate, color="info")
        span(v-if="!loadingResult && !recommendation.length") No Data
        v-flex(v-if="!loadingResult && recommendation.length" v-for="id in recommendation", :key="id", lg3, md4, sm6, xs12)
          v-movie(:movie-id="id")
</template>

<script>
import Movie from '~/components/Movie'

export default {
  components: {
    'v-movie': Movie
  },
  data() {
    return {
      userMovies: {
        model: [],
        items: [],
        search: '',
        loading: false
      },
      loadingResult: false,
      recommendation: []
    }
  },
  watch: {
    'userMovies.search'(word) {
      if (!word) return
      this.queryFilm(word, this.userMovies)
    },
    'userMovies.model'(model) {
      this.$axios.$get('/api/collaborative-filtering', {
        params: {
          data: JSON.stringify(this.userMovies.model)
        }
      }).then((data) => {
        this.recommendation = data
      })
    }
  },
  methods: {
    queryFilm(word, obj) {
      obj.loading = true
      this.$axios.$get('/api/search-movie', {
        params: { word }
      }).then((data) => {
        obj.items = data.map(({ id, title }) => ({
          text: title,
          value: id
        }))
        obj.loading = false
      })
    }
  }
}
</script>
