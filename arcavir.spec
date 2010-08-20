#
# How to make SOURCE2 and SOURCE3:
#	tar xzf %{SOURCE0}
#	cd arcavir2010
#	. usr/share/arcavir/functions
#	wget -r $httppath/core/
#	cd $httppath/core/
#	tar cjvf arcavir-data-amd64.tar.bz2 linux-amd64
#	tar cjvf arcavir-data-i386.tar.bz2 linux-i386
#
Summary:	An anti-virus utility for Unix
Summary(pl.UTF-8):	Narzędzie antywirusowe dla Uniksów
Name:		arcavir
Version:	2010
Release:	0.4
License:	restricted or commercial (see URL)
Group:		Applications
Source0:	http://bugtraq.arcabit.com/arcavir2010/%{name}%{version}-linux-i386.tar.gz
# Source0-md5:	e49bea370cc312192aa2982ca2bbd2bf
Source1:	http://bugtraq.arcabit.com/arcavir2010/%{name}%{version}-linux-amd64.tar.gz
# Source1-md5:	28c40a3ead8babe9c8e0e565b7b79ea5
Source2:	arcavir-data-i386.tar.bz2
Source3:	arcavir-data-amd64.tar.bz2
Source4:	arcavir.cron
Source5:	arcad.init
Patch0:		%{name}-update.patch
URL:		http://arcabit.pl/
Requires:	coreutils
Requires:	gnupg
Requires:	grep
Requires:	rsync
Requires:	sed
Suggests:	wget
Obsoletes:	arcacmd
Obsoletes:	arcacmd-updater
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arcavir is anti-virus scanner for Unix.

%description -l pl.UTF-8
Arcavir jest skanerem antywirusowym dla systemów uniksowych.

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
%ifarch	%{ix86}
%setup -q -T -b0 -n %{name}%{version}
tar xvf %{SOURCE2}
mv linux-i386 linux
%else
%ifarch	%{x8664}
%setup -q -T -b1 -n %{name}%{version}
tar xvf %{SOURCE3}
mv linux-amd64 linux
%else
echo "Unknown arch?"
exit 1
%endif
%endif
tar xvf base.tar.gz

%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_datadir}/arcavir/{arcacmd,arcad}} \
	$RPM_BUILD_ROOT/var/{cache/arcavir/update,lib/arcavir/bases,spool/arcavir/arcad} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{arcavir,cron.d,rc.d/init.d}

mkdir docs
cat linux/files.txt | while read type dest u g d p file md5 xxx ; do
	[ "$type" = "file" ] || continue
	dfile=$(basename $dest)
	ddir=$(dirname $dest)
	case "$ddir" in
	etc/arcavir)	instdir=$RPM_BUILD_ROOT%{_sysconfdir}/arcavir ;;
	etc/init.d)	instdir=$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d ;;
	*/bin)		instdir=$RPM_BUILD_ROOT%{_bindir} ;;
	*/sbin)		instdir=$RPM_BUILD_ROOT%{_sbindir} ;;
	*/include)	instdir=$RPM_BUILD_ROOT%{_includedir} ;;
	*/lib*)		instdir=$RPM_BUILD_ROOT%{_libdir} ;;
	*/share/arcavir/arcacmd)	instdir=$RPM_BUILD_ROOT%{_datadir}/arcavir/arcacmd ;;
	*/share/arcavir/arcad)		instdir=$RPM_BUILD_ROOT%{_datadir}/arcavir/arcad ;;
	*/man/man1)	instdir=$RPM_BUILD_ROOT%{_mandir}/man1 ;;
	*/man/man5)	instdir=$RPM_BUILD_ROOT%{_mandir}/man5 ;;
	*/man/man8)	instdir=$RPM_BUILD_ROOT%{_mandir}/man8 ;;
	*/share/doc/*)	instdir=docs ;;
	*)
		echo "Don't know what to do with \"$dest\""
		exit 1
		;;
	esac
	install -p linux/$file $instdir/$dfile
done

install -p usr/bin/* $RPM_BUILD_ROOT%{_bindir}
install -p usr/share/arcavir/* $RPM_BUILD_ROOT%{_datadir}/arcavir
install -p var/lib/arcavir/* $RPM_BUILD_ROOT/var/lib/arcavir

install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/arcavir
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/arcad

rm $RPM_BUILD_ROOT%{_bindir}/arcaupdate-propagate*

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- amavis-ng
%addusertogroup -q arcabit amavis

%triggerin -- amavisd-new
%addusertogroup -q arcabit amavis

%triggerin -- amavisd
%addusertogroup -q arcabit amavis

%pre
%groupadd -g 238 arcabit
%useradd -u 238 -d /var/lib/arcavir -s /bin/false -c "ArcaBit Anti Virus Checker" -g arcabit arcabit

%post
/sbin/ldconfig
/sbin/chkconfig --add arcad
%service arcad restart "ArcaBit Antivirus daemon"

%preun
if [ "$1" = "0" ]; then
	%service arcad stop
	/sbin/chkconfig --del arcad
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove arcabit
	%groupremove arcabit
fi

%files
%defattr(644,root,root,755)
%doc docs/{README,README.arcad,README.arcad-protocol,README.update}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcavir/arcacmd-engine.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcavir/arcacmd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcavir/arcad-engine.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcavir/arcad.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/arcavir/arcaupdate.conf
%attr(754,root,root) /etc/rc.d/init.d/arcad
/etc/cron.d/arcavir
%attr(755,root,root) %{_bindir}/arcabt
%attr(755,root,root) %{_bindir}/arcacmd
%attr(755,root,root) %{_bindir}/arcacompat
%attr(755,root,root) %{_bindir}/arcad-scan
%attr(755,root,root) %{_bindir}/arcaupdate
%attr(755,root,root) %{_bindir}/arcaupdate-get
%attr(755,root,root) %{_sbindir}/arcad
%attr(755,root,root) %{_libdir}/lib*.so*
%{_datadir}/arcavir
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(755,arcabit,arcabit) %dir /var/lib/arcavir
%attr(755,arcabit,arcabit) %dir /var/lib/arcavir/bases
/var/lib/arcavir/pubring.gpg
%attr(755,arcabit,arcabit) %dir /var/spool/arcavir
%attr(755,arcabit,arcabit) %dir /var/spool/arcavir/arcad
%attr(755,arcabit,arcabit) %dir /var/cache/arcavir
%attr(755,arcabit,arcabit) %dir /var/cache/arcavir/update

%files devel
%defattr(644,root,root,755)
%doc docs/{README.arcad-api,Makefile,arcad-scan.c}
%{_includedir}/arcadapi.h
