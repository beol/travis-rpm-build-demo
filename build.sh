#!/bin/env bash

set -ev

BASE_DIR=$(dirname $0)

cd $BASE_DIR

spectool -g -R git.spec
rpmbuild -bb git.spec

[[ -n "${GPG_PASSPHRASE}" ]] && find ./rpmbuild/RPMS -type f -name "*.rpm" | \
        xargs -I{} sh -c "./rpm-sign.exp {} && rpm --checksig {}"
