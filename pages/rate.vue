<template lang="pug">
v-layout(column, wrap)
  v-flex
    v-form(ref="form")
      v-autocomplete(
        v-model="genre.model",
        :items="genre.items",
        label="Genre",
        :rules="[rules.required]"
        multiple,
        prepend-icon="mdi-view-dashboard"
      )
      v-text-field(v-model="budget.model", label="Budget", type="number", :rules="[rules.required]", prepend-icon="mdi-currency-usd")
      v-text-field(v-model="revenue.model", label="Revenue", type="number", :rules="[rules.required]", prepend-icon="mdi-currency-usd")
      v-text-field(v-model="runtime.model", label="Runtime", type="number", :rules="[rules.required]", prepend-icon="mdi-clock-outline")
      v-text-field(v-model="releaseYear.model", label="Release Year", type="number", :rules="[rules.required].concat(releaseYear.rules)", prepend-icon="mdi-filmstrip")
      v-autocomplete(
        v-model="cast.model",
        :loading="cast.loading",
        :items="cast.items",
        :search-input.sync="cast.search",
        label="Cast",
        multiple,
        cache-items,
        :rules="[rules.required]",
        prepend-icon="mdi-drama-masks"
      )
      v-autocomplete(
        v-model="crew.model",
        :loading="crew.loading",
        :items="crew.items",
        :search-input.sync="crew.search",
        label="Crew",
        multiple,
        cache-items,
        :rules="[rules.required]",
        prepend-icon="mdi-fountain-pen-tip"
      )
      v-autocomplete(
        v-model="company.model",
        :loading="company.loading",
        :items="company.items",
        :search-input.sync="company.search",
        label="Production Company",
        multiple,
        cache-items,
        :rules="[rules.required]",
        prepend-icon="mdi-domain"
      )
    v-btn(color="info", @click="query") query
    v-btn(color="info", @click="jsonDialog = true") paste json
  v-flex(align-self-center)
    v-progress-circular(v-if="rating == -1", indeterminate, color="info")
    v-tooltip(v-if="rating >= 0", bottom)
      template
        v-rating(readonly, x-large, center, half-increments, length="10", :value="rating", slot="activator")
      span {{ rating }}
  v-dialog(v-model="jsonDialog", width=500)
    v-card
      v-card-title.headline.grey(primary-title) Paste JSON
      v-card-text
        p Note that 'Cast', 'Crew' and 'Production Company' may not display their name correctly. We don't have an api to query their names. }:\
        v-textarea(v-model="jsonTextarea", :rules="[rules.json]", ref="jsonPaste")
      v-card-actions
        v-btn(@click="pasteJSON") fill!
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
    'company.search'(word) {
      if (!word) return
      this.queryProductionCompany(word, this.productionCompany)
    }
  },
  async asyncData({ $axios, $nuxt }) {
    $nuxt.$loading.start()
    const data = {
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
      company: {
        model: [],
        items: [],
        search: '',
        loading: false
      },
      rules: {
        required: value => (value instanceof Array ? !!value.length : !!value) || 'Required.',
        json(value) {
          try {
            JSON.parse(value)
            return true
          } catch (e) {
            return e.toString()
          }
        }
      },
      rating: -2,
      jsonDialog: false,
      jsonTextarea: ''
    }
    $nuxt.$loading.finish()
    return data
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
      const data = {
        budget: parseInt(this.budget.model),
        revenue: parseInt(this.revenue.model),
        runtime: parseInt(this.runtime.model),
        releaseYear: parseInt(this.releaseYear.model),
        genre: this.genre.model,
        cast: this.cast.model,
        crew: this.crew.model,
        company: this.company.model
      }
      // eslint-disable-next-line
      console.log(data)
      this.$axios.$get('/api/rate-forecast', {
        params: {
          data: JSON.stringify(data)
        }
      }).then(([[data]]) => {
        this.rating = data
      })
    },
    pasteJSON() {
      if (!this.$refs.jsonPaste.validate()) {
        return
      }
      const data = JSON.parse(this.jsonTextarea)
      for (const d of ['budget', 'revenue', 'runtime', 'releaseYear']) {
        if (Number.isSafeInteger(data[d]) || /[0-9]+/.test(data[d])) {
          this[d].model = data[d].toString()
        }
      }
      for (const d of ['genre', 'cast', 'crew', 'company']) {
        if (Array.isArray(data[d]) && data[d].reduce((pv, tv) => pv && (Number.isSafeInteger(tv) || /[0-9]+/.test(tv)), true)) {
          this[d].model = data[d].map(Number)
        }
      }
      this.jsonDialog = false
    }
  }
}
</script>
