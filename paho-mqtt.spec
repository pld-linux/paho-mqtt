#
# Conditional build:
%bcond_without	apidocs		# API documentation

Summary:	Eclipse Paho MQTT C client libraries
Summary(pl.UTF-8):	Biblioteki klienckie C Eclipse Paho MQTT
Name:		paho-mqtt
Version:	1.3.14
Release:	1
License:	EPL v2.0, EDL v1.0
Group:		Libraries
#Source0Download: https://github.com/eclipse-paho/paho.mqtt.c/releases
Source0:	https://github.com/eclipse/paho.mqtt.c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0289af6d1927e148dc7fc1b2b8f26e29
URL:		https://eclipse.dev/paho/
BuildRequires:	cmake >= 3.5
%if %{with apidocs}
BuildRequires:	doxygen
%endif
BuildRequires:	openssl-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Eclipse Paho project provides open-source client implementations
of MQTT and MQTT-SN messaging protocols aimed at new, existing, and
emerging applications for the Internet of Things (IoT).

%description -l pl.UTF-8
Project Eclipse Paho dostarcza mające otwarte źródła implementacje
klienckie protokołów komunikacji MQTT i MQTT-SN, przeznaczonych dla
nowych, istniejących i nadchodzących aplikacji IoT (Internet of
Things).

%package devel
Summary:	Header files for Eclipse Paho MQTT C client libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek klienckich C Eclipse Paho MQTT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header files for Eclipse Paho MQTT C client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Eclipse Paho MQTT C client.

%package apidocs
Summary:	API documentation for Eclipse Paho MQTT C client libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek klienckich C Eclipse Paho MQTT
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Eclipse Paho MQTT C client libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek klienckich C Eclipse Paho MQTT.

%prep
%setup -q -n paho.mqtt.c-%{version}

# some names are too common, package just HTML
%{__sed} -i -e '/^GENERATE_MAN/ s/YES/NO/' doc/DoxyfileV3{Async,Client}API.in

%build
install -d build
cd build
%cmake .. \
	-DPAHO_BUILD_SHARED=TRUE \
	-DPAHO_HIGH_PERFORMANCE=TRUE \
	-DPAHO_WITH_SSL=TRUE \
	%{?with_apidocs:-DPAHO_BUILD_DOCUMENTATION=TRUE}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/samples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/{edl-v10,epl-v20,*.md,*.html}
%if %{with apidocs}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/MQTT*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.md SECURITY.md about.html notice.html edl-v10 epl-v20
%attr(755,root,root) %{_libdir}/libpaho-mqtt3c.so.*.*.*
%ghost %{_libdir}/libpaho-mqtt3c.so.1
%attr(755,root,root) %{_libdir}/libpaho-mqtt3cs.so.*.*.*
%ghost %{_libdir}/libpaho-mqtt3cs.so.1
%attr(755,root,root) %{_libdir}/libpaho-mqtt3a.so.*.*.*
%ghost %{_libdir}/libpaho-mqtt3a.so.1
%attr(755,root,root) %{_libdir}/libpaho-mqtt3as.so.*.*.*
%ghost %{_libdir}/libpaho-mqtt3as.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/MQTTVersion
%{_libdir}/libpaho-mqtt3a.so
%{_libdir}/libpaho-mqtt3c.so
%{_libdir}/libpaho-mqtt3as.so
%{_libdir}/libpaho-mqtt3cs.so
%{_includedir}/MQTT*.h
%{_libdir}/cmake/eclipse-paho-mqtt-c
%{_examplesdir}/%{name}-%{version}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/doc/MQTT*
%endif
