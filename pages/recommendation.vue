<template lang="pug">
v-layout(row, wrap)
  v-flex(xs4)
    v-autocomplete(v-model="form1.genre.model", :items="form1.genre.items", label="Genre", multiple)
    v-autocomplete(v-model="form1.cast.model", :loading="form1.cast.loading", :items="form1.cast.items", :search-input.sync="form1.cast.search", label="Cast", multiple, cache-items)
    v-autocomplete(v-model="form1.crew.model", :loading="form1.crew.loading", :items="form1.crew.items", :search-input.sync="form1.crew.search", label="Crew", multiple, cache-items)
    v-autocomplete(v-model="form1.productionCompany.model", :items="form1.productionCompany.items", label="Production Company", multiple)
    v-autocomplete(v-model="form1.spokenLanguage.model", :items="form1.spokenLanguage.items", label="Spoken Language", multiple)
    v-text-field(v-model="form1.keyword.model", label="Keywords")
    v-btn(color="info", @click="queryForm1") 查找
  v-flex(xs8)
    v-container(grid-list-md, fluid, fill-height)
      v-layout(align-center, justify-center, fill-height, wrap)
        v-progress-circular(v-if="form1.loadingResult", indeterminate, color="info")
        span(v-if="!form1.loadingResult && !form1.result.length") 暂无数据
        v-flex(v-if="!form1.loadingResult && form1.result.length" v-for="(result, ind) in form1.result", :key="ind", lg3, md4, xs6)
          v-card
            v-responsive(:aspect-ratio="3/4")
              v-progress-circular(v-if="!result", indeterminate, color="info")
              v-card-title(v-if="result", primary-title)
                h3
                  a(:href="'https://www.themoviedb.org/movie/' + result.id") {{ result.originalTitle }}
              v-card-actions(v-if="result")
                v-tooltip(bottom)
                  template
                    v-rating(readonly, half-increments, length="10", dense, small, :value="result.voteAverage", slot="activator")
                  span {{ result.voteAverage }}
</template>

<script>
export default {
  watch: {
    'form1.cast.search'(word) {
      if (!word) return
      if (this.form1.cast.model.indexOf(word) !== -1) return
      this.queryCredit(word, this.form1.cast)
    },
    'form1.crew.search'(word) {
      if (!word) return
      if (this.form1.crew.model.indexOf(word) !== -1) return
      this.queryCredit(word, this.form1.crew)
    }
  },
  async asyncData({ $axios }) {
    return {
      form1: {
        genre: {
          model: [],
          items: (await $axios.get('/api/genres')).data.map(([value, text]) => ({ value, text }))
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
          items: (await $axios.get('/api/production-companies')).data.map(([value, text]) => ({ value, text }))
        },
        spokenLanguage: {
          model: [],
          items: (await $axios.get('/api/spoken-languages')).data.sort()
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
    queryForm1() {
      this.form1.loadingResult = true
      // eslint-disable-next-line
      console.log(JSON.stringify({
        genre: this.form1.genre.model,
        cast: this.form1.cast.model,
        crew: this.form1.crew.model,
        production_companies: this.form1.productionCompany.model,
        keywords: this.form1.keyword.model.split(' '),
        spoken_languages: this.form1.spokenLanguage.model
      }))
      this.$axios.get('/api/recommendation1', {
        params: {
          data: {
            genre: this.form1.genre.model,
            cast: this.form1.cast.model,
            crew: this.form1.crew.model,
            production_companies: this.form1.productionCompany.model,
            keywords: this.form1.keyword.model.split(' '),
            spoken_languages: this.form1.spokenLanguage.model
          }
        }
      }).then(({ data }) => {
        this.form1.loadingResult = false
        this.form1.result = new Array(this.form1.length)
        data.forEach((id, ind) => {
          this.$axios.get('/api/get-movie', {
            params: {
              id
            }
          }).then(({ data }) => {
            this.form1.result.splice(ind, 1, data)
          })
        })
      })
    }
  }
}
</script>
