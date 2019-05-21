const Sequelize = require('sequelize')

const sequelize = new Sequelize('itai', 'root', '123456', {
  host: 'localhost',
  dialect: 'mariadb',
  logging: false
})

const Model = Sequelize.Model
class Movie extends Model {}
Movie.init({
  title: Sequelize.CHAR,
  budget: Sequelize.BIGINT,
  revenue: Sequelize.BIGINT,
  overview: Sequelize.TEXT,
  popularity: Sequelize.DOUBLE,
  releaseYear: Sequelize.INTEGER,
  runtime: Sequelize.INTEGER,
  voteAverage: Sequelize.DOUBLE,
  voteCount: Sequelize.INTEGER
}, {
  sequelize,
  modelName: 'movie',
  timestamps: false
})
class Genre extends Model {}
Genre.init({
  genre: Sequelize.CHAR
}, {
  sequelize,
  modelName: 'genre',
  timestamps: false
})
class Keyword extends Model {}
Keyword.init({
  keyword: Sequelize.CHAR
}, {
  sequelize,
  modelName: 'keyword',
  timestamps: false
})
class Credit extends Model {}
Credit.init({
  name: Sequelize.CHAR
}, {
  sequelize,
  modelName: 'credit',
  timestamps: false
})
class ProductionCompany extends Model {}
ProductionCompany.init({
  name: Sequelize.CHAR
}, {
  sequelize,
  modelName: 'production_company',
  timestamps: false
})

Movie.belongsToMany(Genre, { through: 'movie_genre' })
Genre.belongsToMany(Movie, { through: 'movie_genre' })
Movie.belongsToMany(Keyword, { through: 'movie_keyword' })
Keyword.belongsToMany(Movie, { through: 'movie_keyword' })
Movie.belongsToMany(Credit, { as: 'cast', through: 'movie_cast' })
Credit.belongsToMany(Movie, { through: 'movie_cast' })
Movie.belongsToMany(Credit, { as: 'crew', through: 'movie_crew' })
Credit.belongsToMany(Movie, { through: 'movie_crew' })
Movie.belongsToMany(ProductionCompany, { through: 'movie_production_company' })
ProductionCompany.belongsToMany(Movie, { through: 'movie_production_company' })

sequelize.authenticate()

module.exports = {
  sequelize,
  Movie,
  Genre,
  Keyword,
  Credit,
  ProductionCompany
}
