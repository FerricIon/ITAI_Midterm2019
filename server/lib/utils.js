/**
 * python zip
 * @param  {...Array} rows rows to zip
 * @returns {Array} zipped rows
 */
function zip (...rows) {
  return [...rows][0].map((_, c) => [...rows].map(row => row[c]))
}

module.exports = {
  zip
}
