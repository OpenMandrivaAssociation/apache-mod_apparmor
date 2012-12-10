%define rev 907

%define major 1
%define libname %mklibname apparmor %{major}
%define develname %mklibname apparmor -d

Summary:	Fine-grained AppArmor confinement for apache
Name:		apache-mod_apparmor
Version:	2.3
Release:	%mkrel 1.%{rev}.8
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



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.907.8mdv2012.0
+ Revision: 772551
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.907.7
+ Revision: 678253
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.907.6mdv2011.0
+ Revision: 587911
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.907.5mdv2010.1
+ Revision: 516036
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.907.4mdv2010.0
+ Revision: 406517
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.907.3mdv2009.1
+ Revision: 326474
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.907.2mdv2009.1
+ Revision: 325531
- rebuild

* Wed Aug 06 2008 Luiz Fernando Capitulino <lcapitulino@mandriva.com> 2.3-1.907.1mdv2009.0
+ Revision: 264752
- updated to version 2.3

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-1.907.4mdv2009.0
+ Revision: 234615
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-1.907.3mdv2009.0
+ Revision: 215524
- fix rebuild
- fix buildroot

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-1.907.2mdv2008.1
+ Revision: 182821
- rebuild

* Wed Feb 27 2008 Andreas Hasenack <andreas@mandriva.com> 2.1.2-1.907.1mdv2008.1
+ Revision: 175928
- updated apache-mod_apparmor to 2.1.2-907
- copied apparmor into apache-mod_apparmor

* Thu Jan 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1-1.1076.2mdv2008.1
+ Revision: 154124
- rebuild for new perl

* Tue Jan 08 2008 Andreas Hasenack <andreas@mandriva.com> 2.1-1.1076.1mdv2008.1
+ Revision: 146893
- updated to svn revision 1076

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.5mdv2008.0
+ Revision: 91191
- remove more profiles from standard package: they are shipped in their own packages now

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.4mdv2008.0
+ Revision: 91061
- drop rpcbind profile, it's shipped in the rpcbind package now

* Fri Sep 14 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.3mdv2008.0
+ Revision: 85766
- bonobo file is under a noarch libdir
- build dbus and gnome applet packages

* Fri Sep 14 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.1mdv2008.0
+ Revision: 85546
- install perl module in arch dir as the makefile does for x86_64 (doesn't seem right, though)
- make it not require an installed libapparmor-devel to build
- added swig to buildrequires
- added profile for rpcbind
- fix default syslog profile
- obsolete apparmor-docs (manpages are in each package now)
- better place for the LibAppArmor module
- build apache-mod_apparmor package
- install LibAppArmor.pm
- added utils subpackage
- Import apparmor



* Thu Sep 06 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-0.r954.1mdv2008.0
- initial Mandriva package
