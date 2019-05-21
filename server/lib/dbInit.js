/* eslint-disable no-console */
const fs = require('fs-extra')
const Progress = require('progress')
const db = require('./db')

db.sequelize.sync().then(() => {
  // db.Genre.count().then((c) => {
  //   if (c === 0) {
  //     console.log('No data for Genres. Start importing.')
  //     fs.readJSON('../data/genres.json').then(async (data) => {
  //       const bar = new Progress('[:bar] :current/:total :percent :rate/s :eta', {
  //         total: data.length
  //       })
  //       for (const [id, genre] of data) {
  //         await db.Genre.create({ id, genre })
  //         bar.tick()
  //       }
  //       console.log('Done.')
  //     }).catch((e) => {
  //       console.error(e)
  //     })
  //   }
  // })
  // db.Keyword.count().then((c) => {
  //   if (c === 0) {
  //     console.log('No data for Keywords. Start importing.')
  //     fs.readJSON('../data/keywords.json').then(async (data) => {
  //       const bar = new Progress('[:bar] :current/:total :percent :rate/s :eta', {
  //         total: data.length
  //       })
  //       for (const [id, keyword] of data) {
  //         await db.Keyword.create({ id, keyword })
  //         bar.tick()
  //       }
  //       console.log('Done.')
  //     })
  //   }
  // })
  // db.Credit.count().then((c) => {
  //   if (c === 0) {
  //     console.log('No data for Credits. Start importing.')
  //     fs.readJSON('../data/credits.json').then(async (data) => {
  //       const bar = new Progress('[:bar] :current/:total :percent :rate/s :eta', {
  //         total: data.length
  //       })
  //       for (const [id, name] of data) {
  //         await db.Credit.create({ id, name })
  //         bar.tick()
  //       }
  //       console.log('Done.')
  //     })
  //   }
  // })
  // db.ProductionCompany.count().then((c) => {
  //   if (c === 0) {
  //     console.log('No data for Production Companies. Start importing.')
  //     fs.readJSON('../data/productionCompanies.json').then(async (data) => {
  //       const bar = new Progress('[:bar] :current/:total :percent :rate/s :eta', {
  //         total: data.length
  //       })
  //       for (const [id, name] of data) {
  //         await db.ProductionCompany.create({ id, name })
  //         bar.tick()
  //       }
  //       console.log('Done.')
  //     })
  //   }
  // })
  db.Movie.count().then((c) => {
    if (c === 0) {
      fs.readJSON('../data/movies.json').then(async (data) => {
        const bar = new Progress('[:bar] :current/:total :percent :rate/s :eta', {
          total: data.length
        })
        for (const movie of data) {
          const instance = await db.Movie.create({
            id: movie.id,
            title: movie.title,
            budget: movie.budget,
            revenue: movie.revenue,
            overview: movie.overview,
            popularity: movie.popularity,
            releaseYear: new Date(movie.release_date).getFullYear(),
            runtime: movie.runtime,
            voteAverage: movie.vote_average,
            voteCount: movie.vote_count
          })
          for (const { id } of movie.genres) {
            await instance.addGenre(id)
          }
          for (const { id } of movie.keywords) {
            await instance.addKeyword(id)
          }
          for (const { id } of movie.credits.cast) {
            await instance.addCast(id)
          }
          for (const { id, job } of movie.credits.crew) {
            if (job === 'Director' || job === 'Writer' || job === 'Editor') {
              await instance.addCrew(id)
            }
          }
          await instance.save()
          bar.tick()
        }
        console.log('Done.')
      })
    }
  })
})
