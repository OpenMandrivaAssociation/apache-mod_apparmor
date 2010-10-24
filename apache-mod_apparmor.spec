%define rev 907

%define major 1
%define libname %mklibname apparmor %{major}
%define develname %mklibname apparmor -d

Summary:	Fine-grained AppArmor confinement for apache
Name:		apache-mod_apparmor
Version:	2.3
Release:	%mkrel 1.%{rev}.6
License:	LGPL
Group:		System/Servers
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	apache2-mod_apparmor-%{version}-%{rev}.tar.gz
Source1:        B15_mod_apparmor.conf
BuildRequires:  apache-devel
BuildRequires:  libapparmor-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
AppArmor is a security framework that proactively protects the operating system
and applications.

apache-mod_apparmor adds support to apache to provide AppArmor confinement
to individual cgi scripts handled by apache modules like mod_php and mod_perl.
This package is part of a suite of tools that used to be named SubDomain.

%prep
%setup -q -n apache2-mod_apparmor-%{version}

%build
%serverbuild

#%make   LIBAPPARMOR_FLAGS="-L../libapparmor/src/.libs -lapparmor -I../libapparmor/src" \
#        TESTBUILDDIR=$(pwd)

%make TESTBUILDDIR=$(pwd)


%install
rm -rf %{buildroot}

%{makeinstall_std} APXS_INSTALL_DIR=%{_libdir}/apache-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post
if [ -f /var/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/httpd ]; then
                %{_initrddir}/httpd restart 1>&2
        fi
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING.LGPL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/B15_mod_apparmor.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_apparmor.so
%attr(0644,root,root) %{_mandir}/man8/mod_apparmor.8*

