# Pass --without docs to rpmbuild if you don't want the documentation
%global _without_docs 1
%global debug_package %{nil}

Name: 		git
Version: 	2.11.0
Release: 	1%{?dist}
Summary:  	Core git tools
License: 	GPL
Group: 		Development/Tools
URL: 		http://kernel.org/pub/software/scm/git/
Source: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.gz
BuildRequires:	zlib-devel, openssl-devel, curl-devel  %{!?_without_docs:, xmlto, asciidoc > 6.0.3}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	perl-Git = %{version}-%{release}
Requires:	zlib, rsync, less, openssh-clients, expat
Provides:	git-core = %{version}-%{release}
Obsoletes:	git-core <= 1.5.4.2
Obsoletes:	git-p4

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
Requires:       git = %{version}-%{release}, subversion
%description svn
Git tools for importing Subversion repositories.

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
./configure --prefix=/opt/git && \
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     NO_GETTEXT=YesPlease \
     NO_EXPAT=YesPlease \
     NO_TCLTK=YesPlease \
     NO_PYTHON=YesPlease \
     all %{!?_without_docs: doc}

%install
rm -rf $RPM_BUILD_ROOT
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=$RPM_BUILD_ROOT \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'

(find $RPM_BUILD_ROOT%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@)               > bin-man-doc-files
(find $RPM_BUILD_ROOT%{_libexecdir}/git-core -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@)               >> bin-man-doc-files
(find $RPM_BUILD_ROOT%{perl_vendorlib} -type f | sed -e s@^$RPM_BUILD_ROOT@@) >> perl-files
%if %{!?_without_docs:1}0
(find $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT/Documentation -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}
%endif
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
install -m 644 -T contrib/completion/git-completion.bash $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/git

%clean
rm -rf $RPM_BUILD_ROOT

%files -f bin-man-doc-files
%defattr(-,root,root)
%{_datadir}/git-core/
%doc README COPYING Documentation/*.txt
%{!?_without_docs: %doc Documentation/*.html Documentation/howto}
%{!?_without_docs: %doc Documentation/technical}
%{_sysconfdir}/bash_completion.d

%files svn
%defattr(-,root,root)
%{_libexecdir}/git-core/*svn*
%doc Documentation/*svn*.txt
%{!?_without_docs: %{_mandir}/man1/*svn*.1*}
%{!?_without_docs: %doc Documentation/*svn*.html }

%files -n perl-Git -f perl-files
%defattr(-,root,root)

