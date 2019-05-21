const Router = require('koa-router')

const loader = require('./lib/loader')
const processor = require('./lib/processor')

const router = new Router()

router.get('/api/genres', async (ctx) => {
  ctx.body = await loader.allGenres()
})
router.get('/api/keywords', async (ctx) => {
  ctx.body = await loader.allKeywords()
})

router.get('/api/genre-distribution', async (ctx) => {
  ctx.body = await processor.getGenreDistribution()
})
router.get('/api/keyword-distribution', async (ctx) => {
  ctx.body = await processor.getKeywordDistribution()
})

router.get('/api/search-credit', async (ctx) => {
  ctx.body = await processor.searchCredit(ctx.query.word)
})
router.get('/api/search-production-company', async (ctx) => {
  ctx.body = await processor.searchProductionCompany(ctx.query.word)
})
router.get('/api/search-movie', async (ctx) => {
  ctx.body = await processor.searchMovie(ctx.query.word)
})

router.get('/api/movie', async (ctx) => {
  ctx.body = await loader.loadMovie(ctx.query.id)
})

router.get('/api/simple-filtering', (ctx) => {
  ctx.body = processor.simpleFiltering(ctx.query.data)
})
router.get('/api/collaborative-filtering', (ctx) => {
  ctx.body = processor.collaborativeFiltering(ctx.query.data)
})
module.exports = router
