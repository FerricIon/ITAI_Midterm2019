require('./jsDoc')

const fs = require('fs-extra')
const csv = require('csv/lib/sync')

const utils = require('./utils')

function convertToJSON(pathMovies, pathCredits) {
  const csvMovies = fs.readFileSync(pathMovies)
  const csvCredits = fs.readFileSync(pathCredits)

  const rawMovies = csv.parse(csvMovies)
  const rawCredits = csv.parse(csvCredits)

  const SchemaMovie = {
    budget: Number,
    genres: Array,
    homepage: String,
    id: Number,
    keywords: Array,
    original_language: String,
    original_title: String,
    overview: String,
    popularity: Number,
    production_companies: Array,
    production_countries: Array,
    release_date: Date,
    revenue: Number,
    runtime: Number,
    spoken_language: Array,
    status: String,
    tagline: String,
    title: String,
    vote_average: Number,
    vote_count: Number
  }

  let u = utils.zip(rawMovies, rawCredits)
  const schemas = u.shift()

  u = u.map(([movie, credits]) => {
    const obj = {}
    utils.zip(schemas[0], movie).forEach(([k, v]) => {
      if (SchemaMovie[k] === String) {
        obj[k] = v
      } else if (SchemaMovie[k] === Date) {
        obj[k] = new Date(v)
      } else {
        try {
          obj[k] = JSON.parse(v)
        } catch (e) {
          obj[k] = null
        }
      }
    })
    obj.credits = {}
    utils.zip(schemas[1], credits).forEach(([k, v]) => {
      if (k === 'cast' || k === 'crew') {
        obj.credits[k] = JSON.parse(v)
      }
    })
    return obj
  })

  // productionCompanies
  if (!fs.existsSync('../data/productionCompanies.json')) {
    const pcMap = new Map()
    u.forEach(({ production_companies }) => {
      production_companies.forEach(({ id, name }) => {
        pcMap.set(id, name)
      })
    })
    fs.writeFile('../data/productionCompanies.json', JSON.stringify([...pcMap].sort((a, b) => a[0] - b[0])))
  }
  // genres
  if (!fs.existsSync('../data/genres.json')) {
    const gMap = new Map()
    u.forEach(({ genres }) => {
      genres.forEach(({ id, name }) => {
        gMap.set(id, name)
      })
    })
    fs.writeFile('../data/genres.json', JSON.stringify([...gMap].sort((a, b) => a[0] - b[0])))
  }
  // keywords
  if (!fs.existsSync('../data/keywords.json')) {
    const kMap = new Map()
    u.forEach(({ keywords }) => {
      keywords.forEach(({ id, name }) => {
        kMap.set(id, name)
      })
    })
    fs.writeFile('../data/keywords.json', JSON.stringify([...kMap].sort((a, b) => a[0] - b[0])))
  }
  // credits
  if (!fs.existsSync('../data/credits.json')) {
    const cMap = new Map()
    u.forEach(({ credits }) => {
      credits.cast.forEach(({ id, name }) => {
        cMap.set(id, name)
      })
      credits.crew.forEach(({ id, name }) => {
        cMap.set(id, name)
      })
    })
    fs.writeFile('../data/credits.json', JSON.stringify([...cMap].sort((a, b) => a[0] - b[0])))
  }
  // job
  if (!fs.existsSync('../data/jobs.txt')) {
    const jSet = new Set()
    u.forEach((o) => {
      o.credits.crew.forEach((c) => {
        jSet.add(c.job)
      })
    })
    fs.writeFile('../data/jobs.txt', [...jSet].join('\n'))
  }
  // spoken language
  if (!fs.existsSync('../data/spokenLanguages.json')) {
    const sSet = new Set()
    u.forEach(({ spoken_languages }) => {
      spoken_languages.forEach(({ name }) => {
        sSet.add(name)
      })
    })
    fs.writeFile('../data/spokenLanguages.json', JSON.stringify([...sSet]))
  }

  // visualization
  if (!fs.existsSync('../data/visualization.json')) {
    const vU = u.map(o => ({
      genres: o.genres.map(({ id }) => id),
      keywords: o.keywords.map(({ id }) => id),
      releaseYear: o.release_date.getFullYear()
    }))
    fs.writeFile('../data/visualization.json', JSON.stringify(vU))
  }
  // recommendation
  if (!fs.existsSync('../data/recommendation.json')) {
    const acceptableJobs = ['Director', 'Editor']
    const rU = u.map(o => ({
      id: o.id,
      genre: o.genres.map(({ id }) => id),
      cast: o.credits.cast.slice(0, 5).map(({ id }) => id),
      crew: o.credits.crew.filter(o => !!~acceptableJobs.indexOf(o.job)).map(({ id }) => id),
      production_companies: o.production_companies.map(({ id }) => id),
      keywords: o.keywords.map(({ id }) => id),
      spoken_languages: o.spoken_languages.map(({ name }) => name),
      runtime: o.runtime,
      revenue: o.revenue,
      rate_average: o.vote_average,
      rate_count: o.vote_count,
      popularity: o.popularity
    }))
    fs.writeFile('../data/recommendation.json', JSON.stringify(rU))
  }
  // rate
  if (!fs.existsSync('../data/rate.json')) {
    const acceptableJobs = ['Director', 'Editor']
    const rU = u.map(o => ({
      id: o.id,
      budge: o.budget,
      revenue: o.revenue,
      runtime: o.runtime,
      releaseYear: o.release_date.getFullYear(),
      genre: o.genres.map(({ id }) => id),
      cast: o.credits.cast.slice(0, 5).map(({ id }) => id),
      crew: o.credits.crew.filter(o => !!~acceptableJobs.indexOf(o.job)).map(({ id }) => id),
      production_companies: o.production_companies.map(({ id }) => id),
      rate_average: o.vote_average,
      rate_count: o.vote_count
    }))
    fs.writeFile('../data/rate.json', JSON.stringify(rU))
  }
}

/**
 * data loader
 * @param {String} path path of CSV file
 * @returns {Movie []}
 */
function csvLoadMovies(pathInfo, pathCredits) {
  const csvText = fs.readFileSync(pathInfo)
  const raw = csv.parse(csvText)

  const schema = {
    budget: Number,
    genres: Array,
    homepage: String,
    id: Number,
    keywords: Array,
    original_language: String,
    original_title: String,
    overview: String,
    popularity: Number,
    production_companies: Array,
    production_countries: Array,
    release_date: Date,
    revenue: Number,
    runtime: Number,
    spoken_language: Array,
    status: String,
    tagline: String,
    title: String,
    vote_average: Number,
    vote_count: Number
  }
  const schemas = raw.shift()
  const data = raw.map((row) => {
    const obj = {}
    utils.zip(schemas, row).forEach((kv) => {
      if (schema[kv[0]] === String) {
        obj[kv[0]] = kv[1]
      } else if (schema[kv[0]] === Date) {
        obj[kv[0]] = new Date(kv[1])
      } else {
        // Number & Array
        obj[kv[0]] = JSON.parse(kv[1] || '-1')
      }
    })

    return obj
  })

  return data
}
function movies() {
  return new Map(require('../data/movies.json').map(o => [o.id, o]))
}
function credits() {
  return new Map(require('../data/credits.json'))
}
function genres() {
  return new Map(require('../data/genres.json'))
}
function keywords() {
  return new Map(require('../data/keywords.json'))
}
function productionCompanies() {
  return new Map(require('../data/productionCompanies.json'))
}
function spokenLanguages() {
  return require('../data/spokenLanguages.json')
}

function visualization() {
  return require('../data/visualization.json')
}
function recommendation1() {
  return new Map(require('../data/recommendation.json').map(o => [o.id, o]))
}

module.exports = {
  convertToJSON,
  movies,
  credits,
  genres,
  keywords,
  productionCompanies,
  spokenLanguages,
  visualization,
  recommendation1,
  csvLoadMovies
}
