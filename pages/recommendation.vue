<template lang="pug">
v-layout(:row="$vuetify.breakpoint.lgAndUp", :column="$vuetify.breakpoint.mdAndDown", wrap)
  v-flex(lg4)
    v-autocomplete(
      v-model="form1.genre.model",
      :items="form1.genre.items",
      label="Genre",
      multiple
    )
    v-autocomplete(
      v-model="form1.cast.model",
      :loading="form1.cast.loading",
      :items="form1.cast.items",
      :search-input.sync="form1.cast.search",
      label="Cast",
      multiple,
      cache-items
    )
    v-autocomplete(
      v-model="form1.crew.model",
      :loading="form1.crew.loading",
      :items="form1.crew.items",
      :search-input.sync="form1.crew.search",
      label="Crew",
      multiple,
      cache-items
    )
    v-autocomplete(
      v-model="form1.productionCompany.model",
      :loading="form1.productionCompany.loading",
      :items="form1.productionCompany.items",
      :search-input.sync="form1.productionCompany.search",
      label="Production Company",
      multiple
      cache-items
    )
    v-text-field(v-model="form1.keyword.model", label="Keywords")
    v-btn(color="info", @click="queryForm1") Query
  v-flex(lg8)
    v-container(grid-list-md, fluid, fill-height)
      v-layout(align-center, justify-center, fill-height, wrap)
        v-progress-circular(v-if="form1.loadingResult", indeterminate, color="info")
        span(v-if="!form1.loadingResult && !form1.result.length") No Data
        v-flex(v-if="!form1.loadingResult && form1.result.length" v-for="id in form1.result", :key="id", lg3, md4, sm6, xs12)
          v-movie(:movie-id="id")
</template>

<script>
import Movie from '~/components/Movie'

export default {
  components: {
    'v-movie': Movie
  },
  watch: {
    'form1.cast.search'(word) {
      if (!word) return
      this.queryCredit(word, this.form1.cast)
    },
    'form1.crew.search'(word) {
      if (!word) return
      this.queryCredit(word, this.form1.crew)
    },
    'form1.productionCompany.search'(word) {
      if (!word) return
      this.queryProdunctionCompany(word, this.form1.productionCompany)
    }
  },
  async asyncData({ $axios }) {
    return {
      form1: {
        genre: {
          model: [],
          items: (await $axios.$get('/api/genres')).map(({ id, genre }) => ({
            value: id,
            text: genre
          }))
        },
        cast: {
          model: [],
          items: [],
          search: '',
          loading: false
        },
        crew: {
          model: [],
          items: [],
          search: '',
          loading: false
        },
        productionCompany: {
          model: [],
          loading: false,
          search: '',
          items: []
        },
        keyword: {
          model: ''
        },
        loadingResult: false,
        result: []
      }
    }
  },
  methods: {
    queryCredit(word, obj) {
      obj.loading = true
      this.$axios.$get('/api/search-credit', {
        params: {
          word
        }
      }).then((data) => {
        obj.items = data.map(({ id, name }) => ({
          text: name,
          value: id
        }))
        obj.loading = false
      })
    },
    queryProdunctionCompany(word, obj) {
      obj.loading = true
      this.$axios.get('/api/search-production-company', {
        params: {
          word
        }
      }).then(({ data }) => {
        obj.items = data.map(({ id, name }) => ({
          text: name,
          value: id
        }))
        obj.loading = false
      })
    },
    queryForm1() {
      this.form1.loadingResult = true
      this.$axios.get('/api/simple-filtering', {
        params: {
          data: {
            genre: this.form1.genre.model,
            cast: this.form1.cast.model,
            crew: this.form1.crew.model,
            production_companies: this.form1.productionCompany.model,
            keywords: this.form1.keyword.model.split(' '),
            spoken_languages: []
          }
        }
      }).then(({ data }) => {
        this.form1.loadingResult = false
        this.form1.result = data
      })
    }
  }
}
</script>
