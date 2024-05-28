# BinBuddy

Developing a model that detects trash and suggests the appropriate bin involves several steps, from model training to integrating it with a mobile app.


- The project configuration: the single source of truth is `.env`
  - `.envrc` tells `direnv` to load the `.env` as environment variables
  - `params.py` then loads all these variable in python, and should not be changed manually anymore
