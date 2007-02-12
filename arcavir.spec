# TODO:
# - fix version information (2.6 is Linux version)
# - move databases to /var/lib, fix paths in arcaupdate
#
Summary:	An anti-virus utility for Unix
Summary(pl.UTF-8):   Narzędzie antywirusowe dla Uniksów
Name:		arcacmd
Version:	2.6
Release:	0.1
License:	restricted or commercial (see COPYING* files)
Group:		Applications
Source0:	http://arcabit.pl/download/linux/%{name}-linux%{version}-bundle-20060731.tgz
# Source0-md5:	ffc56e252fbb05b60fa80255140a81d8
URL:		http://arcabit.pl/
Requires:	libstdc++ >= 5:3.4
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arcavir is anti-virus scanner for Unix.

%description -l pl.UTF-8
Arcavir jest skanerem antywirusowym dla systemów uniksowych.

%package bases
Summary:	Arcavir Antivirus databases
Summary(pl.UTF-8):   Bazy antywirusowe arcavir
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description bases
This package contains antivirus databases.

%description bases -l pl.UTF-8
Pakiet ten zawiera bazy antywirusowe.

%package updater
Summary:	Arcavir Antivirus database updater
Summary(pl.UTF-8):   Aktualizator baz antywirusowych arcavir
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	/usr/bin/wget
Requires:	bc
Requires:	coreutils

%description updater
This package contains antivirus databases updater.

%description updater -l pl.UTF-8
Pakiet ten zawiera aktualizator baz antywirusowych.

%prep
%setup -q -n inst

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/arcacmd/bases/tmp,%{_bindir},%{_sbindir},%{_mandir}/man1,%{_sysconfdir}}

cd files
install arcacmd $RPM_BUILD_ROOT%{_bindir}
install arcaupdate $RPM_BUILD_ROOT%{_sbindir}
cd docs
gzip -dc arcacmd.1.gz >$RPM_BUILD_ROOT%{_mandir}/man1/arcacmd.1
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
%lang(fr) %doc files/docs/COPYING.{commercial,free}.fr
%lang(pl) %doc files/docs/COPYING.{commercial,free}.pl
%attr(755,root,root) %{_bindir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcacmdg.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/pl_ascii.atr
%{_mandir}/man1/*

%files bases
%defattr(644,root,root,755)
%verify(not md5 mtime size) %{_datadir}/%{name}/abase?.dat

%files updater
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/arcaupdate
