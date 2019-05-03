require('./jsDoc')

/**
 * get genre distribution
 * @param {Movie []} movies
 * @returns {GenreDecadeDistribution []}
 */
function getGenreDistribution(movies) {
  const releaseYears = movies.map(({ releaseYear }) => releaseYear).filter(a => !!a)
  const step = 5
  const yearRange = [Math.min(...releaseYears), Math.max(...releaseYears)].map(year => year - year % step)
  const decades = [...(new Array((yearRange[1] - yearRange[0]) / step + 1)).keys()].map(k => k * step + yearRange[0])

  const distribution = new Map()
  movies.forEach((movie) => {
    if (movie.releaseYear === null) {
      return
    }
    const decade = movie.releaseYear - (movie.releaseYear % step)
    movie.genres.forEach((gid) => {
      if (!distribution.has(gid)) {
        distribution.set(gid, new Map(decades.map(k => [k, 0])))
      }
      const genreMap = distribution.get(gid)
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
 * @param {Movie []} movies
 * @returns {KeywordDecadeDistribution []}
 */
function getKeywordDistribution(movies) {
  const distribution = new Map()
  movies.forEach((movie) => {
    if (movie.releaseYear === null) {
      return
    }
    const decade = movie.releaseYear - (movie.releaseYear % 10)
    if (!distribution.has(decade)) {
      distribution.set(decade, new Map())
    }
    const decadeDistribution = distribution.get(decade)
    movie.keywords.forEach((kid) => {
      decadeDistribution.set(kid, (decadeDistribution.get(kid) || 0) + 1)
    })
  })

  return [...distribution].map(([decade, decadeMap]) => ({
    decade,
    distribution: [...decadeMap].map(([id, count]) => ({ id, count }))
  })).sort((a, b) => a.decade - b.decade)
}

module.exports = {
  getGenreDistribution,
  getKeywordDistribution
}
