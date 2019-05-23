<template lang="pug">
v-layout(column, wrap)
  v-flex
    v-form(ref="form")
      v-autocomplete(
        v-model="genre.model",
        :items="genre.items",
        label="Genre",
        :rules="[rules.required]"
        multiple
      )
      v-text-field(v-model="budget.model", label="Budget", type="number", :rules="[rules.required]")
      v-text-field(v-model="revenue.model", label="Revenue", type="number", :rules="[rules.required]")
      v-text-field(v-model="runtime.model", label="Runtime", type="number", :rules="[rules.required]")
      v-text-field(v-model="releaseYear.model", label="Release Year", type="number", :rules="[rules.required].concat(releaseYear.rules)")
      v-autocomplete(
        v-model="cast.model",
        :loading="cast.loading",
        :items="cast.items",
        :search-input.sync="cast.search",
        label="Cast",
        multiple,
        cache-items,
        :rules="[rules.required]"
      )
      v-autocomplete(
        v-model="crew.model",
        :loading="crew.loading",
        :items="crew.items",
        :search-input.sync="crew.search",
        label="Crew",
        multiple,
        cache-items,
        :rules="[rules.required]"
      )
      v-autocomplete(
        v-model="productionCompany.model",
        :loading="productionCompany.loading",
        :items="productionCompany.items",
        :search-input.sync="productionCompany.search",
        label="Production Company",
        multiple,
        cache-items,
        :rules="[rules.required]"
      )
    v-btn(color="info", @click="query") query
  v-flex(align-self-center)
    v-progress-circular(v-if="rating == -1", indeterminate, color="info")
    v-tooltip(v-if="rating >= 0", bottom)
      template
        v-rating(readonly, x-large, center, half-increments, length="10", :value="rating", slot="activator")
      span {{ rating }}
</template>

<script>
import Movie from '~/components/Movie'

export default {
  components: {
    'v-movie': Movie
  },
  watch: {
    'cast.search'(word) {
      if (!word) return
      this.queryCredit(word, this.cast)
    },
    'crew.search'(word) {
      if (!word) return
      this.queryCredit(word, this.crew)
    },
    'productionCompany.search'(word) {
      if (!word) return
      this.queryProductionCompany(word, this.productionCompany)
    }
  },
  async asyncData({ $axios }) {
    return {
      genre: {
        model: [],
        items: (await $axios.$get('/api/genres')).map(({ id, genre }) => ({
          value: id,
          text: genre
        }))
      },
      budget: {
        model: ''
      },
      revenue: {
        model: ''
      },
      runtime: {
        model: ''
      },
      releaseYear: {
        model: '',
        rules: [
          value => (value >= 1900 && value <= 2019) || 'Between 1900 and 2019.'
        ]
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
        items: [],
        search: '',
        loading: false
      },
      rules: {
        required: value => (value instanceof Array ? !!value.length : !!value) || 'Required.'
      },
      rating: -2
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
    queryProductionCompany(word, obj) {
      obj.loading = true
      this.$axios.$get('/api/search-production-company', {
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
    query() {
      if (!this.$refs.form.validate()) {
        return
      }
      this.rating = -1
      const void5 = [0, 0, 0, 0, 0]
      let data = [parseInt(this.budget.model) / 100000, parseInt(this.revenue.model) / 100000, parseInt(this.runtime.model), parseInt(this.releaseYear.model)]
      data = data.concat(this.genre.model.concat(void5).slice(0, 5))
      data = data.concat(this.cast.model.concat(void5).slice(0, 5))
      data = data.concat(this.crew.model.concat(void5).slice(0, 5))
      data = data.concat(this.productionCompany.model.concat(void5).slice(0, 5))
      this.$axios.$get('/api/rate-forecast', {
        params: {
          data: JSON.stringify(data)
        }
      }).then((data) => {
        this.rating = data
      })
    }
  }
}
</script>
