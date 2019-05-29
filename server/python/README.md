# python
Python modules.
Note that Node.js communicate with the python modules by spawning a child_process and build a pipe to the module's `stdin`. Thus the modules get input of JSON format from `input()`, and the backend appilication get return value from `stdout`.

## Useful Information
- `Collaborative Filtering/` stores data and source code to get the sim matrix.
- `Collaborative Filtering.py` provides api to use Collaborative Filtering.
- `nmodel` is the trained keras model.
- `Rate Forecast Training.py` trains a neural network and store it in `nmodel`.
- `Rate Forecast.py` provides api to use Rate Forecast.
- `Simple Filtering.py` provides api to use Simple Filtering.