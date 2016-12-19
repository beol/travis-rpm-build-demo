#!/bin/bash

yum -y install gcc \
    rpm-build \
    zlib-devel \
    openssl-devel \
    curl-devel \
    perl-ExtUtils-MakeMaker

rpmbuild -bc -vv /code/git.spec
