FROM centos:centos6
MAINTAINER Leo Laksmana <beol@laksmana.com>

RUN yum -y install \
           curl-devel \
           expect \
           gcc \
           openssl-devel \
           perl-Error \
           perl-ExtUtils-MakeMaker \
           rpm-build \
           rpmdevtools \
           zlib-devel

WORKDIR /etc/pki/rpm-gpg
COPY RPM-GPG-KEY-laksmana .
RUN rpm --import RPM-GPG-KEY-laksmana

RUN useradd -m -d /source -u 1000 rpmbuild

WORKDIR /source
USER rpmbuild
