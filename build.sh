#!/bin/bash

BASE_DIR=$(dirname $0)

yum -y install gcc \
       rpm-build \
       zlib-devel \
       openssl-devel \
       curl-devel \
       perl-ExtUtils-MakeMaker \
       perl-Error

mkdir -p $BASE_DIR/rpmbuild/{SPECS,SOURCES,BUILD,RPMS,SRPMS,BUILDROOT}

curl -s -L -o $BASE_DIR/rpmbuild/SOURCES/git-2.11.0.tar.gz http://kernel.org/pub/software/scm/git/git-2.11.0.tar.gz

rpmbuild -bb --define "_topdir ${BASE_DIR}/rpmbuild" --without docs $BASE_DIR/git.spec
