// const path1 = '../../csv/tmdb_5000_movies.csv'
// const path2 = '../../csv/tmdb_5000_credits.csv'

// const u = require('./loader').convertToJSON

// u(path1, path2)

const { rec1GetMovie } = require('./processor')
const { recommendation1 } = require('./loader')
console.log(rec1GetMovie(173931))
