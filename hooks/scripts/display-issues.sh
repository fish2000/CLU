#!/usr/bin/env bash

source ~/.bash_config.d/private.bash

hub="/usr/local/bin/hub"

if [[ -x $hub ]]; then
    exec $hub issue
fi