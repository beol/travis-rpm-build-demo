# Pass --without docs to rpmbuild if you don't want the documentation
%global _without_docs 1
%global debug_package %{nil}
%global _exec_prefix /opt/git

Name: 		git
Version: 	2.11.0
Release: 	1%{?dist}
Summary:  	Core git tools
License: 	GPL
Group: 		Development/Tools
URL: 		http://kernel.org/pub/software/scm/git/
Source: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.gz
BuildRequires:	zlib-devel >= 1.2, openssl-devel, curl-devel  %{!?_without_docs:, xmlto, asciidoc > 6.0.3}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	perl-Git = %{version}-%{release}
Requires:	zlib >= 1.2, rsync, less, openssh-clients
Provides:	git-core = %{version}-%{release}
Obsoletes:	git-core <= 1.5.4.2
Obsoletes:	git-p4

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(Error)
BuildRequires:  perl(ExtUtils::MakeMaker)

%description -n perl-Git
Perl interface to Git

%prep
%setup -q

%build
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     configure
./configure --prefix=%{_prefix} \
            --exec_prefix=%{_exec_prefix} \
            --without-expat \
            --without-tcltk \
            --without-python
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     all %{!?_without_docs: doc} \
     NO_GETTEXT=YesPlease

%install
rm -rf $RPM_BUILD_ROOT
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=$RPM_BUILD_ROOT \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc} \
     NO_GETTEXT=YesPlease

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/gitweb

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
install -m 644 -T contrib/completion/git-completion.bash $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/git

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat -<<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/profile.d/git.sh
pathmunge %{_bindir} after

source %{_sysconfdir}/bash_completion.d/git
EOF

(find $RPM_BUILD_ROOT%{_bindir} -type f | sed -e s@^$RPM_BUILD_ROOT@@)               > bin-man-doc-files
(find $RPM_BUILD_ROOT%{_libexecdir}/git-core -type f  | sed -e s@^$RPM_BUILD_ROOT@@) >> bin-man-doc-files
(find $RPM_BUILD_ROOT%{_datadir}/git-core -type f  | sed -e s@^$RPM_BUILD_ROOT@@)    >> bin-man-doc-files
(find $RPM_BUILD_ROOT%{_sysconfdir} -type f  | sed -e s@^$RPM_BUILD_ROOT@@)          >> bin-man-doc-files
(find $RPM_BUILD_ROOT%{perl_vendorlib} -type f | sed -e s@^$RPM_BUILD_ROOT@@)        >> perl-files
%if %{!?_without_docs:1}0
(find $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT/Documentation -type f | sed -e s@^$RPM_BUILD_ROOT@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f bin-man-doc-files
%defattr(-,root,root)
%doc README.md COPYING Documentation/*.txt
%{!?_without_docs: %doc Documentation/*.html Documentation/howto}
%{!?_without_docs: %doc Documentation/technical}

%files -n perl-Git -f perl-files
%defattr(-,root,root)

