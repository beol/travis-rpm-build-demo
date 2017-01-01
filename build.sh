#!/bin/env bash

BASE_DIR=$(dirname $0)

rpmbuild -bb --define 'debug_package %{nil}' ${BASE_DIR}/git.spec
