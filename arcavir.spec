Summary:	An anti-virus utility for Unix
Summary(pl):	Antywirusowe narzêdzie dla Uniksów
Name:		arcacmd
Version:	2.6
Release:	1
License:	see COPYING
Group:		Applications
Source0:	http://arcabit.pl/download/linux/%{name}-linux%{version}-bundle-20060731.tgz
# Source0-md5:	ffc56e252fbb05b60fa80255140a81d8
URL:		http://arcabit.pl/
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arcavir is anti-virus scanner for Unix.

%description -l pl
Arcavir jest skanerem antywirusowym dla systemów uniksowych.

%package bases
Summary:	Arcavir Antivirus databases
Summary(pl):	Bazy antywirusowe arcavir
Group:		Applications

%description bases
This package contains antivirus databases.

%description bases -l pl
Pakiet ten zawiera bazy antywirusowe.

%package updater
Summary:	Arcavir Antivirus database updater
Summary(pl):	Aktualizator baz antywirusowych arcavir
Group:		Applications
Requires:	/usr/bin/wget
Requires:	bc
Requires:	coreutils

%description updater
This package contains antivirus databases updater.

%description updater -l pl
Pakiet ten zawiera aktualizator baz antywirusowych.

%prep
%setup -q -n inst

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/arcacmd/bases/tmp,%{_bindir},%{_sbindir},%{_mandir}/man1,%{_sysconfdir}}

cd files/
install arcacmd $RPM_BUILD_ROOT%{_bindir}
install arcaupdate $RPM_BUILD_ROOT%{_sbindir}
cd docs
install arcacmd.1.gz $RPM_BUILD_ROOT%{_mandir}/man1
cd ..
install arcacmdg.conf $RPM_BUILD_ROOT%{_sysconfdir}
install arcacmdl.conf.template $RPM_BUILD_ROOT%{_sysconfdir}

for f in lang/* bases/*; do
	install $f $RPM_BUILD_ROOT%{_datadir}/%{name}
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc files/docs/COPYING.*
%{_mandir}/man1/*
%{_datadir}/%{name}/pl_ascii.atr
%attr(755,root,root) %{_bindir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcacmdg.conf

%files bases
%defattr(644,root,root,755)
%verify(not md5 mtime size) %{_datadir}/%{name}/abase?.dat

%files updater
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/arcaupdate
