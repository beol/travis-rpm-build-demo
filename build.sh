#!/bin/bash

BASE_DIR=$(dirname $0)

VERSION=$(grep Version ${BASE_DIR}/git.spec | awk '{print $2}')

yum -y install gcc \
       rpm-build \
       zlib-devel \
       openssl-devel \
       curl-devel \
       perl-ExtUtils-MakeMaker \
       perl-Error

mkdir -p $BASE_DIR/rpmbuild/{SPECS,SOURCES,BUILD,RPMS,SRPMS,BUILDROOT}

curl -s -L -o $BASE_DIR/rpmbuild/SOURCES/git-$VERSION.tar.gz http://kernel.org/pub/software/scm/git/git-$VERSION.tar.gz

rpmbuild -bb --define 'debug_package %{nil}' --define "_topdir ${BASE_DIR}/rpmbuild" --without docs $BASE_DIR/git.spec

yum localinstall -y $BASE_DIR/rpmbuild/RPMS/x86_64/git-$VERSION-*.rpm $BASE_DIR/rpmbuild/RPMS/x86_64/perl-Git-$VERSION-*.rpm

/opt/git/bin/git --version
