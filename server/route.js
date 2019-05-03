const Router = require('koa-router')

const loader = require('./lib/loader')
const processor = require('./lib/processor')

const router = new Router()

router.get('/api/genres', (ctx) => {
  ctx.body = [...loader.genres()]
})
router.get('/api/genre-distribution', (ctx) => {
  ctx.body = processor.getGenreDistribution(loader.visualization())
})
router.get('/api/keywords', (ctx) => {
  ctx.body = [...loader.keywords()]
})
router.get('/api/keyword-distribution', (ctx) => {
  ctx.body = processor.getKeywordDistribution(loader.visualization())
})

module.exports = router
