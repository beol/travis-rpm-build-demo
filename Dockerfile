FROM centos:centos6
MAINTAINER Leo Laksmana <beol@laksmana.com>

COPY RPM-GPG-KEY-laksmana /etc/pki/rpm-gpg/RPM-GPG-KEY-laksmana
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-laksmana

RUN yum -y install \
           curl-devel \
           expect \
           gcc \
           openssl-devel \
           perl-Error \
           perl-ExtUtils-MakeMaker \
           rpm-build \
           rpmdevtools \
           zlib-devel \
    && \
    yum clean all

RUN useradd -m -u 1000 rpmbuild

WORKDIR /home/rpmbuild
USER rpmbuild
COPY .rpmmacros .gnupg ./
