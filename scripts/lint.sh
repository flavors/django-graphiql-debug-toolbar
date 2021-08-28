#!/usr/bin/env bash

export SOURCE_FILES="graphiql_debug_toolbar tests"

set -e
set -x

flake8 $SOURCE_FILES
black --check $SOURCE_FILES
isort --check-only $SOURCE_FILES
