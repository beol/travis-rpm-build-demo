#!/bin/bash

yum -y install gcc \
    rpm-build \
    zlib-devel \
    openssl-devel \
    curl-devel \
    perl-ExtUtils-MakeMaker

mkdir -p /code/rpmbuild/{SPECS,SOURCES,BUILD,RPMS,SRPMS,BUILDROOT}

curl -s -L -o /code/rpmbuild/SOURCES/git-2.11.0.tar.gz http://kernel.org/pub/software/scm/git/git-2.11.0.tar.gz

rpmbuild -bc -vv --define '_topdir /code/rpmbuild' /code/git.spec
