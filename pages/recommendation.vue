<template lang="pug">
v-layout(column)
  v-flex(xs6)
    v-autocomplete(v-model="rec1.genre", :items="rec1.genres", label="Genre", multiple)
  v-divider
  v-flex(xs6) a
</template>

<script>
export default {
  async asyncData({ $axios }) {
    return {
      rec1: {
        genre: '',
        genres: (await $axios.get('/api/genres')).data
      }
    }
  }
}
</script>
