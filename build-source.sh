#!/bin/env bash

set -ev

BASE_DIR=$(dirname $0)

cd $BASE_DIR

spectool -g -R git.spec
rpmbuild -bs git.spec

