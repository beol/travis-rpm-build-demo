%global _name   git
%global _ver %{?_version}%{!?_version:2.11.0}
%global _xver %(echo %{_ver} | cut -d. -f1,2)
%global _prefix /opt/%{name}

Name: 		%{_name}%(echo %{_xver} | sed "s,\.,,")
Version: 	%{_ver}
Release: 	%{?_release}%{!?_release:0a}%{?dist}
Summary:  	Fast Version Control System
License: 	GPLv2
Group: 		Development/Tools
URL: 		http://git-scm.com/
Source: 	http://kernel.org/pub/software/scm/git/%{_name}-%{version}.tar.gz
BuildRequires:	zlib-devel >= 1.2, openssl-devel, curl-devel
BuildRoot:	%{_tmppath}/%{_name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	zlib >= 1.2, rsync, less, openssh-clients

Provides:   git = %{version}-%{release}
Provides:	git-core = %{version}-%{release}
Obsoletes:	git-core <= 1.5.4.2

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

%prep
%setup -q -n %{_name}-%{version}

%build
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     configure
./configure --prefix=%{_prefix} \
            --without-expat \
            --without-tcltk \
            --without-python
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     all \
     NO_GETTEXT=YesPlease

%install
rm -rf $RPM_BUILD_ROOT
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=$RPM_BUILD_ROOT \
     INSTALLDIRS=vendor install \
     NO_GETTEXT=YesPlease

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'

find $RPM_BUILD_ROOT%{_bindir} -type f | grep -E "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-p4" | xargs rm -f
find $RPM_BUILD_ROOT%{_libexecdir}/git-core -type f | grep -E "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-p4" | xargs rm -f
find $RPM_BUILD_ROOT%{_usr}/share/doc -type f | grep -E "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-p4" | xargs rm -f

rm -rf $RPM_BUILD_ROOT%{_datadir}/gitweb
rm -rf $RPM_BUILD_ROOT%{_datadir}/man
rm -rf $RPM_BUILD_ROOT%{_datadir}/perl5/vendor_perl/Git/SVN*
rm -rf $RPM_BUILD_ROOT%{_libdir}
rm -rf $RPM_BUILD_ROOT%{_mandir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/git-core/contrib
install -m 644 -t $RPM_BUILD_ROOT%{_datadir}/git-core/contrib contrib/completion/git-completion.bash contrib/completion/git-prompt.sh


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.md COPYING Documentation/*.txt
%{_prefix}

