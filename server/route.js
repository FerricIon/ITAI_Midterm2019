const Router = require('koa-router')

const loader = require('./lib/loader')
const processor = require('./lib/processor')

const router = new Router()

router.get('/api/genres', (ctx) => {
  ctx.body = [...loader.genres()]
})
router.get('/api/keywords', (ctx) => {
  ctx.body = [...loader.keywords()]
})
router.get('/api/production-companies', (ctx) => {
  ctx.body = [...loader.productionCompanies()]
})
router.get('/api/spoken-languages', (ctx) => {
  ctx.body = loader.spokenLanguages()
})

router.get('/api/genre-distribution', (ctx) => {
  ctx.body = processor.getGenreDistribution(loader.visualization())
})
router.get('/api/keyword-distribution', (ctx) => {
  ctx.body = processor.getKeywordDistribution(loader.visualization())
})

router.get('/api/search-credit', (ctx) => {
  ctx.body = processor.searchForCredit(ctx.query.word)
})
router.get('/api/recommendation1', (ctx) => {
  ctx.body = processor.recommendation1(ctx.query.data)
})
router.get('/api/get-movie', (ctx) => {
  ctx.body = processor.rec1GetMovie(parseInt(ctx.query.id))
})
module.exports = router
