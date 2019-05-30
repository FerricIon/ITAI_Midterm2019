<template lang="pug">
v-card
  v-responsive(:aspect-ratio="2/3")
    v-container(fill-height)
      div.cover(:style="style", @click.stop="showDetail = true")
      v-icon.magnify-icon(large) mdi-magnify
      v-layout(fill-height, column, align-center, justify-space-between, style="z-index: 2; pointer-events: none;")
        v-flex(xs1)
          a.movie-title(:href="'https://www.themoviedb.org/movie/' + movie.id", style="pointer-events: auto;") {{ movie.title }}
        v-flex(xs1)
          v-tooltip(bottom, style="pointer-events: auto;")
            template
              v-rating(readonly, color="white", half-increments, length="5", dense, small, :value="movie.voteAverage / 2", slot="activator")
            span {{ movie.voteAverage }}
  v-btn(v-if="closable", absolute, dark, fab, bottom, right, small, color="grey", @click="$emit('close')")
    v-icon mdi-close
  v-dialog(v-model="showDetail", width="700px")
    v-card
      v-card-title.headline(center) {{ movie.title }}
      v-card-text
        v-container(style="padding: 0")
          v-layout
            v-flex(xs4)
              v-img(:src="`/posters/${movie.id}.jpg`")
            v-flex(xs8)
              v-list(two-line)
                v-list-tile
                  v-list-tile-avatar
                    v-icon mdi-star
                  v-list-tile-content
                    v-list-tile-title Vote Average
                    v-list-tile-sub-title {{ movie.voteAverage }}
                v-list-tile
                  v-list-tile-avatar
                    v-icon mdi-filmstrip
                  v-list-tile-content
                    v-list-tile-title Release Year
                    v-list-tile-sub-title {{ movie.releaseYear }}
                v-list-tile
                  v-list-tile-avatar
                    v-icon mdi-currency-usd
                  v-list-tile-content
                    v-list-tile-title Budget / Revenue
                    v-list-tile-sub-title {{ movie.budget }} / {{ movie.revenue }}
                v-list-tile
                  v-list-tile-avatar
                    v-icon mdi-clock-outline
                  v-list-tile-content
                    v-list-tile-title Runtime
                    v-list-tile-sub-title {{ movie.runtime }}
          v-flex(xs12)
            v-item-group
              v-list-tile
                v-list-tile-avatar
                  v-icon mdi-view-dashboard
                v-list-tile-content
                  v-list-tile-title Genres
              v-item(v-for="{ genre } in movie.genres", :key="genre")
                v-chip {{ genre }}
            v-item-group
              v-list-tile
                v-list-tile-avatar
                  v-icon mdi-key
                v-list-tile-content
                  v-list-tile-title Keywords
              v-item(v-for="{ keyword } in movie.keywords", :key="keyword")
                v-chip {{ keyword }}
            v-item-group
              v-list-tile
                v-list-tile-avatar
                  v-icon mdi-drama-masks
                v-list-tile-content
                  v-list-tile-title Cast
              v-item(v-for="{ name } in movie.cast", :key="name")
                v-chip {{ name }}
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
      },
      showDetail: false
    }
  },
  computed: {
    style() {
      return {
        background: 'linear-gradient(to top, rgba(0, 0, 0, .8), transparent 20%, transparent 70%, rgba(0, 0, 0, .8)) no-repeat 0px 0px, url(/posters/' + this.movieId + '.jpg)',
        'background-size': 'contain'
      }
    }
  },
  async mounted() {
    this.movie.id = this.movieId
    this.movie = await this.$axios.$get('/api/movie', {
      params: {
        id: this.movie.id
      }
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
.cover {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
  z-index: 1;
  transition: all .5s;
  transform: scale(1)
}
.cover:hover {
  filter: blur(4px) brightness(.6);
  transform: scale(1.1);
  cursor: pointer;
}
.magnify-icon {
  position: absolute;
  color: white;
  pointer-events: none;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 4;
  opacity: 0;
  transition: all .5s;
}
.cover:hover + .magnify-icon {
  opacity: 1;
}
</style>
