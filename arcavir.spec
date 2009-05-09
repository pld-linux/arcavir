Summary:	An anti-virus utility for Unix
Summary(pl.UTF-8):	Narzędzie antywirusowe dla Uniksów
Name:		arcacmd
Version:	2009
Release:	1
License:	restricted or commercial (see COPYING* files)
Group:		Applications
Source0:	http://bugtraq.arcabit.com/devel/arcavir2009-server/arcavir%{version}-server-linux-i386.tar.gz
# Source0-md5:	28f20af0e39a7ebacbc1e798dd51ce69
Source1:	arcavir.cron
Patch0:		arcavir-bases-path.patch
Patch1:		arcavir-init-chkconfig.patch
URL:		http://arcabit.pl/
Requires:	libstdc++ >= 5:3.4
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arcavir is anti-virus scanner for Unix.

%description -l pl.UTF-8
Arcavir jest skanerem antywirusowym dla systemów uniksowych.

%package updater
Summary:	Arcavir Antivirus database updater
Summary(pl.UTF-8):	Aktualizator baz antywirusowych arcavir
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	/usr/bin/wget
Requires:	bc
Requires:	coreutils

%description updater
This package contains antivirus databases updater.

%description updater -l pl.UTF-8
Pakiet ten zawiera aktualizator baz antywirusowych.

%package devel
Summary:	arcavir - Development header files and libraries
Summary(pl.UTF-8):	arcavir - Pliki nagłówkowe i biblioteki dla programistów
Group:		Development/Libraries

%description devel
This package contains the development header files and libraries
necessary to develop arcavir client applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do kompilacji aplikacji
klienckich arcavir.

%prep
%setup -q -n arcavir%{version}-server
tar xvf data.tar.gz

%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/arcabit/lang/cmd,%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8},%{_sysconfdir}/rc.d/init.d,var/cache/arcabit/bases,var/spool/arcad,%{_libdir},%{_includedir}}
install -d $RPM_BUILD_ROOT/var/lib/arcavir/bases $RPM_BUILD_ROOT%{_sysconfdir}/cron.d

install usr/lib/lib*.so* $RPM_BUILD_ROOT%{_libdir}
install usr/sbin/arcad $RPM_BUILD_ROOT%{_sbindir}
install usr/bin/* $RPM_BUILD_ROOT%{_bindir}
install usr/share/arcabit/uninstall-data $RPM_BUILD_ROOT%{_datadir}/arcabit
install usr/share/arcabit/lang/cmd/* $RPM_BUILD_ROOT%{_datadir}/arcabit/lang/cmd/
install usr/include/* $RPM_BUILD_ROOT%{_includedir}
install etc/*.conf $RPM_BUILD_ROOT%{_sysconfdir}
install etc/init.d/arcad $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install usr/include/* $RPM_BUILD_ROOT%{_includedir}
install usr/share/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install usr/share/man/man5/* $RPM_BUILD_ROOT%{_mandir}/man5
install usr/share/man/man8/* $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/arcavir

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so*
%attr(755,root,root) %{_sbindir}/arcad
%attr(755,root,root) %{_bindir}/arcacompat
%attr(755,root,root) %{_bindir}/arcad-scan
%attr(755,root,root) %{_bindir}/arcacmd
%doc %{_datadir}/arcabit/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcacmd-scanner.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcacmd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcad.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcad-scanner.conf
%config %{_sysconfdir}/arcacmd-default.conf
%config %{_sysconfdir}/arcascanner-default.conf
%attr(754,root,root) /etc/rc.d/init.d/arcad
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(755,arcabit,arcabit) %dir /var/lib/arcavir
%attr(755,arcabit,arcabit) %dir /var/lib/arcavir/bases

%files updater
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/arcaupdate
/etc/cron.d/arcavir

%files devel
%defattr(644,root,root,755)
%{_includedir}/arcadapi.h

%pre
%groupadd -g 238 arcabit
%useradd -u 238 -d /tmp -s /bin/false -c "Arcavir Anti Virus Checker" -g arcabit arcabit
