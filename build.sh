#!/bin/env bash

set -ev

BASE_DIR=$(dirname $0)

rpmbuild -bb ${BASE_DIR}/git.spec

find ${BASE_DIR}/rpmbuild/RPMS -type f -name "*.rpm" | xargs -I{} expect ${BASE_DIR}/rpm-sign.exp {}

find ${BASE_DIR}/rpmbuild/RPMS -type f -name "*.rpm" | xargs -I{} rpm --checksig {}
