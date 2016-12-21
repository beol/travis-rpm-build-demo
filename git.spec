# Pass --without docs to rpmbuild if you don't want the documentation
%global _name   git
%global _prefix /opt/git

Name: 		%{_name}211
Version: 	2.11.0
Release: 	0%{?dist}
Summary:  	Core git tools
License: 	GPL
Group: 		Development/Tools
URL: 		http://kernel.org/pub/software/scm/git/
Source: 	http://kernel.org/pub/software/scm/git/%{_name}-%{version}.tar.gz
BuildRequires:	zlib-devel >= 1.2, openssl-devel, curl-devel  %{!?_without_docs:, xmlto, asciidoc > 6.0.3}
BuildRoot:	%{_tmppath}/%{_name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	zlib >= 1.2, rsync, less, openssh-clients
Provides:	git-core = %{version}-%{release}
Obsoletes:	git-core <= 1.5.4.2
Obsoletes:	git-p4

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
     all %{!?_without_docs: doc} \
     NO_PERL=YesPlease \
     NO_GETTEXT=YesPlease

%install
rm -rf $RPM_BUILD_ROOT
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=$RPM_BUILD_ROOT \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc} \
     NO_PERL=YesPlease \
     NO_GETTEXT=YesPlease

%if %{!?_without_docs:1}0
(find $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT/Documentation -type f | sed -e s@^$RPM_BUILD_ROOT@@ -e 's/$/*/' )
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}
%endif
rm -rf $RPM_BUILD_ROOT%{_datadir}/gitweb

mkdir -p $RPM_BUILD_ROOT%{_datadir}/git-core/contrib
install -m 644 -t $RPM_BUILD_ROOT%{_datadir}/git-core/contrib contrib/completion/git-completion.bash contrib/completion/git-prompt.sh


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.md COPYING Documentation/*.txt
%{!?_without_docs: %doc Documentation/*.html Documentation/howto}
%{!?_without_docs: %doc Documentation/technical}
%{_prefix}

