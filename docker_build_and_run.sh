#!/usr/bin/bash

docker build -t mdstar .

docker run -it --rm -v "$(pwd)":/workspace mdstar
