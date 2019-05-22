const db = require('./db')

/**
 * Get all genres and their id.
 * @returns {Genre []} Genres.
 */
async function allGenres() {
  const data = await db.Genre.findAll()
  return data
}
/**
 * Get all Keywords and their id.
 * @returns {Keyword []} Keywords.
 */
async function allKeywords() {
  const data = await db.Keyword.findAll()
  return data
}

/**
 * Search a movie by its id.
 * @param {Number} id Movie id.
 * @returns {Movie} The movie.
 */
async function loadMovie(id) {
  const data = await db.Movie.findOne({
    where: { id },
    include: [
      {
        model: db.Genre,
        attributes: ['genre']
      },
      {
        model: db.Keyword,
        attributes: ['keyword']
      },
      {
        model: db.ProductionCompany,
        attributes: ['name']
      },
      {
        model: db.Credit,
        as: 'crew',
        attributes: ['name']
      },
      {
        model: db.Credit,
        as: 'cast',
        attributes: ['name']
      }
    ]
  })
  return data
}

module.exports = {
  allGenres,
  allKeywords,

  loadMovie
}
