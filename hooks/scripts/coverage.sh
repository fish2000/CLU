#!/usr/bin/env bash

pushd $PROJECT_BASE
    
    nox -s codecov
    
popd