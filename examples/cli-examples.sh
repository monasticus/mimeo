#!/bin/bash

# Simple
mimeo examples/1-introduction/01-basic.json

# Custom output
mimeo examples/1-introduction/01-basic.json -o stdout
mimeo examples/1-introduction/01-basic.json --raw

# Custom directory and file name
mimeo examples/1-introduction/01-basic.json -d basic-data -f some-entity

# Customized xml declaration and indent
mimeo examples/1-introduction/01-basic.json -x true -i 4

# HTTP customization
mimeo examples/1-introduction/01-basic.json -o http -H localhost -p 8080 -E /data -U admin -P admin
mimeo examples/1-introduction/01-basic.json -o http -e local
mimeo examples/1-introduction/01-basic.json -o http -e local --http-envs-file config/environments.json
mimeo examples/1-introduction/01-basic.json -o http -e local -E /v2/data
mimeo examples/1-introduction/01-basic.json -o http -e local -U custom-user -P custom-password
