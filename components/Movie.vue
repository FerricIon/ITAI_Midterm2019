<template lang="pug">
v-card
  v-responsive(:aspect-ratio="2/3")
    v-img(:src="`/posters/${movie.id}.jpg`", aspect-ratio="0.66667")
      v-container.movie-card(fill-height)
        v-layout(fill-height, column, align-center, justify-space-between)
          v-flex(xs1)
            a.movie-title(:href="'https://www.themoviedb.org/movie/' + movie.id") {{ movie.title }}
          v-flex(xs1)
            v-tooltip(bottom)
              template
                v-rating(readonly, color="white", half-increments, length="5", dense, small, :value="movie.voteAverage / 2", slot="activator")
              span {{ movie.voteAverage }}
  v-btn(v-if="closable", absolute, dark, fab, bottom, right, small, color="grey", @click="$emit('close')")
    v-icon mdi-close
</template>

<script>
export default {
  props: {
    movieId: {
      type: Number,
      default: 0
    },
    closable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      movie: {
        id: 0,
        title: '',
        voteAverage: 0
      }
    }
  },
  async mounted() {
    this.movie.id = this.movieId
    const { title, voteAverage } = await this.$axios.$get('/api/movie', {
      params: {
        id: this.movie.id
      }
    })
    Object.assign(this.movie, {
      title, voteAverage
    })
  }
}
</script>

<style scoped>
.movie-title {
  color: white;
  font-weight: 700;
  text-decoration: none;
}
.movie-card {
  background-image: linear-gradient(to top, black, transparent 20%, transparent 70%, black);
}
</style>
