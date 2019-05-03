const path1 = '../../csv/tmdb_5000_movies.csv'
const path2 = '../../csv/tmdb_5000_credits.csv'

const u = require('./loader').convertToJSON

u(path1, path2)
