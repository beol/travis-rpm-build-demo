#!/bin/bash

yum -y install gcc rpm-build zlib-devel openssl-devel curl-devel perl-ExtUtils-MakeMaker

curl -L https://www.kernel.org/pub/software/scm/git/git-2.11.0.tar.gz | tar xzf -

cd git-2.11.0 && make configure && ./configure && make all NO_EXPAT=YesPlease NO_TCLTK=YesPlease NO_GETTEXT=YesPlease
