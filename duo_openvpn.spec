%define name	duo_openvpn
%define version	0.5.1
%define release 1
%define prefix	/usr

%define mybuilddir %{_builddir}/%{name}-%{version}-root

Summary:	Duo two-factor authentication for OpenVPN
Name:		%{name}
Version:	%{version}
License:	BSD
Release:	%{release}
Packager:	Jan Schaumann <jschauma@etsy.com>
Group:		Utilities/Misc
Source:		%{name}-%{version}.tar.gz
BuildRoot:	/tmp/%{name}-%{version}-root

Requires:	python26, perl, perl-JSON-XS, perl-Digest-HMAC, perl-URI

%description
Duo provides simple two-factor authentication as a service via:

* Phone callback
* SMS-delivered one-time passcodes
* Duo mobile app to generate one-time passcodes
* Duo mobile app for smartphone push authentication
* Duo hardware token to generate one-time passcodes

This package provides the OpenVPN authentication plugin and scripts.

%prep
%setup -q

%setup
mkdir -p %{mybuilddir}%{prefix}/bin
mkdir -p %{mybuilddir}%{prefix}/lib
mkdir -p %{mybuilddir}%{prefix}/share/duo

%build
make

%install
cp ca_certs.pem %{mybuilddir}%{prefix}/share/duo/ca_certs.pem
cp %{name}.pl %{mybuilddir}%{prefix}/share/duo/%{name}.pl
cp %{name}.py %{mybuilddir}%{prefix}/share/duo/%{name}.py
cp %{name}.so %{mybuilddir}%{prefix}/lib/%{name}.so
cp %{name}_composite.so %{mybuilddir}%{prefix}/lib/%{name}_composite.so
cp https_wrapper.py %{mybuilddir}%{prefix}/share/duo/https_wrapper.py
ln -s %{prefix}/share/duo/%{name}.py %{mybuilddir}%{prefix}/bin/%{name}

%files
%defattr(0755,root,root)
%{prefix}/bin/%{name}
%{prefix}/lib/%{name}.so
%{prefix}/lib/%{name}_composite.so
%{prefix}/share/duo/ca_certs.pem
%{prefix}/share/duo/%{name}.pl
%{prefix}/share/duo/%{name}.py
%attr(0644,root,root)%{prefix}/share/duo/https_wrapper.py

%changelog
* Fri Nov 16 2012 Jan Schaumann <jschauma@etsy.com>
- bump cache to 8 days, but do not refresh

* Fri Oct 10 2012 Jan Schaumann <jschauma@etsy.com>
- allow the plugin to cache username,IP pairs for a certain time without
  re-authenticating with Duo; this allows connections from particularly
  flakey networks to reconnect seemlessly without user interactions;
  NOTE: this explicitly circumvents the authentication mechanism!  Only
  use this if you know what you are doing!

* Wed Oct 10 2012 Jan Schaumann <jschauma@etsy.com>
- rename some variable to be less confusing; no functional change

* Thu Aug 30 2012 Jan Schaumann <jschauma@etsy.com>
- allow fallback to another form of authentication if connections to Duo's
  servers fail

* Mon Aug 27 2012 Jan Schaumann <jschauma@etsy.com>
- ignore SIGCHLD to avoid one zombie per authentication

* Tue Jul 17 2012 Jan Schaumann <jschauma@etsy.com>
- install two modules, one for 'composite' password, one regular

* Mon Jul 09 2012 Jan Schaumann <jschauma@etsy.com>
- first rpm version
