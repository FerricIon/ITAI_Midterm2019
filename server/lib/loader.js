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
  if (!fs.existsSync('./production_companies.json')) {
    const pcMap = new Map()
    u.forEach(({ production_companies }) => {
      production_companies.forEach(({ id, name }) => {
        pcMap.set(id, name)
      })
    })
    fs.writeFile('production_companies.json', JSON.stringify([...pcMap].sort((a, b) => a[0] - b[0])))
  }
  // genres
  if (!fs.existsSync('./genres.json')) {
    const gMap = new Map()
    u.forEach(({ genres }) => {
      genres.forEach(({ id, name }) => {
        gMap.set(id, name)
      })
    })
    fs.writeFile('genres.json', JSON.stringify([...gMap].sort((a, b) => a[0] - b[0])))
  }
  // keywords
  if (!fs.existsSync('./keywords.json')) {
    const kMap = new Map()
    u.forEach(({ keywords }) => {
      keywords.forEach(({ id, name }) => {
        kMap.set(id, name)
      })
    })
    fs.writeFile('keywords.json', JSON.stringify([...kMap].sort((a, b) => a[0] - b[0])))
  }
  // credits
  if (!fs.existsSync('credits.json')) {
    const cMap = new Map()
    u.forEach(({ credits }) => {
      credits.cast.forEach(({ id, name }) => {
        cMap.set(id, name)
      })
      credits.crew.forEach(({ id, name }) => {
        cMap.set(id, name)
      })
    })
    fs.writeFile('credits.json', JSON.stringify([...cMap].sort((a, b) => a[0] - b[0])))
  }

  // visualization
  if (!fs.existsSync('./visualization.json')) {
    const vU = u.map(o => ({
      genres: o.genres.map(({ id }) => id),
      keywords: o.keywords.map(({ id }) => id),
      releaseYear: o.release_date.getFullYear()
    }))
    fs.writeFile('visualization.json', JSON.stringify(vU))
  }
  // recommendation
  
  // vote

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
function credits() {
  return new Map(require('./credits.json'))
}
function genres() {
  return new Map(require('./genres.json'))
}
function keywords() {
  return new Map(require('./keywords.json'))
}
function productionCompanies() {
  return new Map(require('./production_companies.json'))
}
function visualization() {
  return require('./visualization.json')
}

module.exports = {
  convertToJSON,
  credits,
  genres,
  keywords,
  productionCompanies,
  visualization,
  csvLoadMovies
}
