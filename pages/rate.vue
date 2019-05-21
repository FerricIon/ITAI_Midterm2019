<template lang="pug">
v-layout(col, wrap)
  v-flex(xs-6)
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
      cache-items
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
      :items="productionCompany.model",
      :search-input.sync="productionCompany.search",
      label="Production Company",
      multiple,
      cache-items,
      :rules="[rules.required]"
    )
</template>

<script>
import Movie from '~/components/Movie'

export default {
  components: {
    'v-movie': Movie
  },
  data() {
    return {
      genre: {
        model: [],
        items: []
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
      }
    }
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
  methods: {
    queryCredit(word, obj) {
      obj.loading = true
      this.$axios.get('/api/search-credit', {
        params: {
          word
        }
      }).then(({ data }) => {
        obj.items = data.map(([value, text]) => ({
          text,
          value
        }))
        obj.loading = false
      })
    },
    queryProductionCompany(word, obj) {
      obj.loading = true
      this.$axios.get('/api/search-production-company', {
        params: {
          word
        }
      }).then(({ data }) => {
        obj.items = data.map(([value, text]) => ({
          text,
          value
        }))
        obj.loading = false
      })
    }
  }
}
</script>
