/**
 * @typedef {Object} Genre
 * @property {Number} id
 * @property {String} name
 *
 * @typedef {Object} Keyword
 * @property {Number} id
 * @property {String} name
 *
 * @typedef {Object} ProductionCompany
 * @property {Number} id
 * @property {String} name
 *
 * @typedef {Object} ProductionCountry
 * @property {String} iso_3166_1
 * @property {String} name
 *
 * @typedef {Object} SpokenLanguage
 * @property {String} iso_639_1
 * @property {String} name
 *
 * @typedef {Object} Movie
 * @property {Number} budget
 * @property {Genre []} genres
 * @property {String} homepage
 * @property {Number} id
 * @property {Keyword []} keywords
 * @property {String} original_language
 * @property {String} original_title
 * @property {String} overview
 * @property {Number} popularity
 * @property {ProductionCompany []} production_companies
 * @property {ProductionCountry []} production_countries
 * @property {Date} release_date
 * @property {Number} revenue
 * @property {Number} runtime
 * @property {SpokenLanguage []} spoken_language
 * @property {String} status
 * @property {String} tagline
 * @property {String} title
 * @property {Number} vote_average
 * @property {Number} vote_count
 *
 * @typedef {Object} GenreCount
 * @property {String} genre
 * @property {Number} count
 *
 * @typedef {Object} GenreDecadeDistribution
 * @property {Number} decade
 * @property {GenreCount} distribution
 *
 * @typedef {Object} KeywordCount
 * @property {String} keyword
 * @property {Number} count
 *
 * @typedef {Object} KeywordDecadeDistribution
 * @property {Number} decade
 * @property {KeywordCount []} distribution
 */
