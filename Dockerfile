FROM centos:centos6

RUN yum -y install \
           curl-devel \
           gcc \
           openssl-devel \
           perl-Error \
           perl-ExtUtils-MakeMaker \
           rpm-build \
           zlib-devel

RUN useradd -m -d /source -u 1000 rpmbuild

USER rpmbuild
