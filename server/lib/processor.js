/* eslint-disable no-console */
require('./jsDoc')
const Sequelize = require('sequelize')

const db = require('./db')

/**
 * get genre distribution
 * @returns {GenreDecadeDistribution []}
 */
async function getGenreDistribution() {
  const YEAR_STEP = 5

  const data = await db.Movie.findAll({
    attributes: ['releaseYear'],
    include: [{
      model: db.Genre,
      attributes: ['id']
    }]
  })
  const releaseYears = data.map(movie => movie.releaseYear)
  const yearRange = [Math.min(...releaseYears), Math.max(...releaseYears)].map(year => year - year % YEAR_STEP)
  const decades = [...(new Array((yearRange[1] - yearRange[0]) / YEAR_STEP + 1)).keys()].map(k => k * YEAR_STEP + yearRange[0])

  const distribution = new Map()
  data.forEach((movie) => {
    if (movie.releaseYear === null) {
      return
    }
    const decade = movie.releaseYear - (movie.releaseYear % YEAR_STEP)
    movie.genres.forEach(({ id }) => {
      if (!distribution.has(id)) {
        distribution.set(id, new Map(decades.map(k => [k, 0])))
      }
      const genreMap = distribution.get(id)
      genreMap.set(decade, genreMap.get(decade) + 1)
    })
  })
  return [...distribution].map(([id, genreMap]) => ({
    id,
    distribution: [...genreMap].map(([decade, count]) => ({ decade, count })).sort((a, b) => a.decade - b.decade),
    count: [...genreMap].reduce((pv, v) => (pv + v[1]), 0)
  })).sort((a, b) => b.count - a.count)
}
/**
 * get keywords by ten years
 * @returns {KeywordDecadeDistribution []}
 */
async function getKeywordDistribution() {
  const data = await db.Movie.findAll({
    attributes: ['releaseYear'],
    include: [{
      model: db.Keyword,
      attributes: ['id']
    }]
  })
  const distribution = new Map()
  data.forEach((movie) => {
    if (movie.releaseYear === null) {
      return
    }
    const decade = movie.releaseYear - (movie.releaseYear % 10)
    if (!distribution.has(decade)) {
      distribution.set(decade, new Map())
    }
    const decadeDistribution = distribution.get(decade)
    movie.keywords.forEach(({ id }) => {
      decadeDistribution.set(id, (decadeDistribution.get(id) || 0) + 1)
    })
  })

  return [...distribution].map(([decade, decadeMap]) => ({
    decade,
    distribution: [...decadeMap].map(([id, count]) => ({ id, count }))
  })).sort((a, b) => a.decade - b.decade)
}

/**
 * Search a credit with part of his name.
 * @param {String} word Part of the credits's name.
 * @returns {Credit []} Credits found. Up to 20.
 */
async function searchCredit(word) {
  const data = await db.Credit.findAll({
    where: {
      name: {
        [Sequelize.Op.substring]: word
      }
    },
    limit: 20
  })
  return data
}
/**
 * Search a movie with part of its title.
 * @param {String} word Part of the movie's title.
 * @returns {Movie []} Movies found. Up to 20.
 */
async function searchMovie(word) {
  const data = await db.Movie.findAll({
    where: {
      title: {
        [Sequelize.Op.substring]: word
      }
    },
    limit: 20
  })
  return data
}
/**
 * Search a production company with part of its name.
 * @param {String} word Part of the production company's name.
 * @returns {ProductionCompany []} Production Companies found. Up to 20.
 */
async function searchProductionCompany(word) {
  const data = await db.ProductionCompany.findAll({
    where: {
      name: {
        [Sequelize.Op.substring]: word
      }
    },
    limit: 20
  })
  return data
}

/**
 * Simple filtering to recommend movies.
 * @param {Movie []} data Query info.
 * @returns {Number []} Id of movies recommended.
 */
function simpleFiltering(data) {
  const { spawnSync } = require('child_process')
  const fileName = 'Simple Filtering.py'

  const { stdout, stderr } = spawnSync('python', [fileName], {
    cwd: './server/python',
    input: data
  })
  if (stderr.length) {
    console.error(`Error in '${fileName}':\n${stderr.toString()}`)
    return 'error'
  } else {
    return stdout.toString()
  }
}
/**
 * Collaborative filtering to recommend movies.
 * @param {Number []} data Given id of movies.
 * @returns {Number []} Id of movies recommended.
 */
function collaborativeFiltering(data) {
  const { spawnSync } = require('child_process')
  const fileName = 'Collaborative Filtering.py'

  const { stdout, stderr } = spawnSync('python', [fileName], {
    cwd: './server/python',
    input: data
  })
  if (stderr.length) {
    console.error(`Error in '${fileName}':\n${stderr.toString()}`)
    return 'error'
  } else {
    return stdout.toString()
  }
}
function rateForecast(data) {
  const { spawnSync } = require('child_process')
  const fileName = 'Rate Forecast.py'

  const { stdout, stderr } = spawnSync('python', [fileName], {
    cwd: './server/python',
    input: data
  })
  // if (stderr.length) {
  //   console.error(`Error in '${fileName}':\n${stderr.toString()}`)
  //   return 'error'
  // } else {
  return stdout.toString()
  // }
}

module.exports = {
  getGenreDistribution,
  getKeywordDistribution,

  searchCredit,
  searchMovie,
  searchProductionCompany,

  simpleFiltering,
  collaborativeFiltering,
  rateForecast
}
