# Movie Data Analysis and A Model of Movie Commendation

This repository is for our [website](http://104.248.157.18:3000/). Issues are welcomed.

## How to run it locally
### Environment Requirement
- Node.js
- Python3
- MariaDB

### Dependencies
#### Python
`pip install -r requirements.txt`
Including
- nltk
- numpy
- tensorflow

Besides, you need to install NLTK Corpus Wordnet according to the [manual](https://www.nltk.org/data.html).
For example, run this command after installing the dependencies.
`python -m nltk.downloader wordnet`

#### Node.js
`yarn` or `npm install`

### Data Import
Due to the fact that we use MariaDB as our database, you need to import data in.
- Go to directory `/server/data/`
- Log in your MariaDB
- Run `source sql.sql`
We have crawled the posters needed for better user interface. Download [posters.zip](http://104.248.157.18:3000/posters.zip) and unzip to `/static/posters/`.

### Configure
You may need to enter correct username and password to connect to MariaDB.
Config at `/server/lib/db.js`.

### Run
```bash
yarn build
yarn start
```
or
```bash
npm run build
npm  start
```

## Possible Issues
- The recommendation and rate forecast don't work?
  Please check your python version and whether the dependencies have been installed correctly. Note that the backend calls `python` directly other than `python3` or check the version. Can be modified in `/server/lib/processor.js`.

## More Information
Refer to the `READNE.md`s in the folders (but only `/server/` needs revision }:\\).
