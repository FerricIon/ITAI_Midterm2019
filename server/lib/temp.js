const db = require('./db')
const processor = require('./processor')

processor.getGenreDistribution().then((aaa) => {
  console.log(aaa)
}).catch((e) => {
  console.error(e)
})
