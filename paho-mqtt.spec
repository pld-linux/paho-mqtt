Summary:	Eclipse Paho MQTT C client
Name:		paho-mqtt
Version:	1.1.0
Release:	1
License:	EPL-1.0 and EDL-1.0
Group:		Libraries
Source0:	https://github.com/eclipse/paho.mqtt.c/archive/v1.1.0/%{name}-%{version}.tar.gz
# Source0-md5:	ec635e5c4487d9bf1a12d00322b74038
URL:		http://www.eclipse.org/paho/
BuildRequires:	cmake >= 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Eclipse Paho project provides open-source client implementations
of MQTT and MQTT-SN messaging protocols aimed at new, existing, and
emerging applications for the Internet of Things (IoT).

%package devel
Summary:	Header files for Eclipse Paho MQTT C client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Eclipse Paho MQTT C client
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Eclipse Paho MQTT C client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Eclipse Paho MQTT C client.

%package static
Summary:	Static Eclipse Paho MQTT C client library
Summary(pl.UTF-8):	Statyczna biblioteka Eclipse Paho MQTT C client
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Eclipse Paho MQTT C client library.

%description static -l pl.UTF-8
Statyczna biblioteka Eclipse Paho MQTT C client.

%prep
%setup -q -n paho.mqtt.c-%{version}

%build
install -d build
cd build
%cmake ..

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# src/CMakeLists.txt needs patching
# INSTALL( ... LIBRARY DESTINATION lib)
%if "%{_lib}" != "lib"
install -d $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_prefix}/lib/* $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md about.html notice.html
%attr(755,root,root) %{_libdir}/libpaho-mqtt3c.so.*.*.*
%ghost %{_libdir}/libpaho-mqtt3c.so.1
%attr(755,root,root) %{_libdir}/libpaho-mqtt3a.so.*.*.*
%ghost %{_libdir}/libpaho-mqtt3a.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/MQTTVersion
%{_includedir}/MQTTAsync.h
%{_includedir}/MQTTClient.h
%{_includedir}/MQTTClientPersistence.h
%{_libdir}/libpaho-mqtt3a.so
%{_libdir}/libpaho-mqtt3c.so
