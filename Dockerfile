FROM centos:centos6

RUN yum -y install \
           curl-devel \
           expect \
           gcc \
           openssl-devel \
           perl-Error \
           perl-ExtUtils-MakeMaker \
           rpm-build \
           zlib-devel


WORKDIR /tmp
COPY RPM-GPG-KEY-laksmana .
RUN rpm --import RPM-GPG-KEY-laksmana
RUN rm -f RPM-GPG-KEY-laksmana

RUN useradd -m -d /source -u 1000 rpmbuild

USER rpmbuild
