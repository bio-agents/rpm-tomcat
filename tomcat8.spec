# To Build:
#
# sudo yum -y install rpmdevagents && rpmdev-setuptree
#
# wget -P ~/rpmbuild/SOURCES https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.42/bin/apache-tomcat-8.5.42.tar.gz
#
# wget https://github.com/inab/rpm-tomcat/archive/8.5.42.tar.gz
# tar xf 8.5.42.tar.gz
# cp -p rpm-tomcat-8.5.42/tomcat8.spec ~/rpmbuild/SPECS
# cp -p rpm-tomcat-8.5.42/tomcat8.{init,sysconfig,logrotate} ~/rpmbuild/SOURCES
# rpmbuild -bb ~/rpmbuild/SPECS/tomcat8.spec

%define __jar_repack %{nil}
%define tomcat_home /usr/share/tomcat8
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
Name:       tomcat8
Version:    8.5.42
BuildArch:  noarch
Release:    1
License:    Apache Software License
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    apache-tomcat-%{version}.tar.gz
Source1:    %{name}.init
Source2:    %{name}.sysconfig
Source3:    %{name}.logrotate
Requires:   java, %{name}-lib = %{version}-%{release}
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.

This package contains the base tomcat installation that depends on Oracle's JDK and not
on JPP packages.

%package lib
Group: Development/Compilers
Summary: Libraries needed to run the Tomcat Web container
Requires: %{name} = %{version}-%{release}

%description lib
Libraries needed to run the Tomcat Web container

%package admin-webapps
Group: System Environment/Applications
Summary: The host-manager and manager web applications for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Group: System Environment/Applications
Summary: The docs web application for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat.

%package examples-webapp
Group: System Environment/Applications
Summary: The examples web application for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description examples-webapp
The examples web application for Apache Tomcat.

%package root-webapp
Group: System Environment/Applications
Summary: The ROOT web application for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description root-webapp
The ROOT web application for Apache Tomcat.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/var/log/%{name}/
cd %{buildroot}/%{tomcat_home}/
ln -s /var/log/%{name}/ logs
cd -

# Put temp in /var/cache and link back.
rm -rf %{buildroot}/%{tomcat_home}/temp
install -d -m 755 %{buildroot}/var/cache/%{name}/temp
cd %{buildroot}/%{tomcat_home}/
ln -s /var/cache/%{name}/temp temp
cd -

# Put work in /var/cache and link back.
rm -rf %{buildroot}/%{tomcat_home}/work
install -d -m 755 %{buildroot}/var/cache/%{name}/work
cd %{buildroot}/%{tomcat_home}/
ln -s /var/cache/%{name}/work work
cd -

# Put conf in /etc/ and link back.
install -d -m 755 %{buildroot}/%{_sysconfdir}/%{name}/Catalina/localhost
mv %{buildroot}/%{tomcat_home}/conf/* %{buildroot}/%{_sysconfdir}/%{name}/
rmdir %{buildroot}/%{tomcat_home}/conf
cd %{buildroot}/%{tomcat_home}/
ln -s %{_sysconfdir}/%{name} conf
cd -

# Put webapps in /var/lib and link back.
install -d -m 755 %{buildroot}/var/lib/%{name}
mv %{buildroot}/%{tomcat_home}/webapps %{buildroot}/var/lib/%{name}
cd %{buildroot}/%{tomcat_home}/
ln -s /var/lib/%{name}/webapps webapps
cd -

# Put lib in /usr/share/java and link back.
install -d -m 755 %{buildroot}/usr/share/java
mv %{buildroot}/%{tomcat_home}/lib %{buildroot}/usr/share/java/%{name}
cd %{buildroot}/%{tomcat_home}/
ln -s /usr/share/java/%{name} lib
cd -

# Put docs in /usr/share/doc
install -d -m 755 %{buildroot}/usr/share/doc/%{name}-%{version}
mv %{buildroot}/%{tomcat_home}/{RUNNING.txt,LICENSE,NOTICE,RELEASE*} %{buildroot}/usr/share/doc/%{name}-%{version}

# Put executables in /usr/bin
rm  %{buildroot}/%{tomcat_home}/bin/*bat
install -d -m 755 %{buildroot}/usr/{bin,sbin}
mv %{buildroot}/%{tomcat_home}/bin/digest.sh %{buildroot}/usr/bin/%{name}-digest
mv %{buildroot}/%{tomcat_home}/bin/agent-wrapper.sh %{buildroot}/usr/bin/%{name}-agent-wrapper

# Drop init script
install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/%{name}.init %{buildroot}/%{_initrddir}/%{name}

# Drop sysconfig script
install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
install    -m 644 %_sourcedir/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# Drop logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
/var/log/%{name}/
/var/cache/%{name}
%dir /var/lib/%{name}/webapps
%defattr(-,root,root)
%{tomcat_home}/*
%attr(0755,root,root) /usr/bin/*
%dir /var/lib/%{name}
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%doc /usr/share/doc/%{name}-%{version}

%files lib
%defattr(0644,root,root,0755)
/usr/share/java/%{name}

%files admin-webapps
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/host-manager
/var/lib/%{name}/webapps/manager

%files docs-webapp
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/docs

%files examples-webapp
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/examples

%files root-webapp
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/ROOT

%post
chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
  service %{name} condrestart >/dev/null 2>&1
fi

%changelog
* Tue Jun 25 2019 José María Fernández <jose.m.fernandez@bsc.es>
- 8.5.42
* Sat May 25 2019 José María Fernández <jose.m.fernandez@bsc.es>
- 8.5.41 (which fixes a deaadlock https://bz.apache.org/bugzilla/show_bug.cgi?id=63251)
* Tue Jan 15 2019 José María Fernández <jose.m.fernandez@bsc.es>
- 8.5.37
* Fri Dec 14 2018 José María Fernández <jose.m.fernandez@bsc.es>
- 8.5.35
* Mon Oct 30 2017 José María Fernández <jose.m.fernandez@bsc.es>
- 8.5.23
* Tue Feb 21 2017 José María Fernández <jmfernandez@cnio.es>
- 7.0.75
* Wed Dec 14 2016 José María Fernández <jmfernandez@cnio.es>
- 7.0.73
* Wed Jun 8 2016 José María Fernández <jmfernandez@cnio.es>
- 7.0.69
* Wed Apr 7 2016 José María Fernández <jmfernandez@cnio.es>
- 7.0.68
* Wed Nov 4 2015 José María Fernández <jmfernandez@cnio.es>
- 7.0.65
* Wed Jul 22 2015 Jeremy McMillan <jeremy.mcmillan@gmail.com>
- 7.0.63
* Mon May 11 2015 Forest Handford <foresthandford+VS@gmail.com>
- 7.0.61
* Thu Sep 4 2014 Edward Bartholomew <edward@bartholomew>
- 7.0.55
* Fri Apr 4 2014 Elliot Kendall <elliot.kendall@ucsf.edu>
- Update to 7.0.53
- Changes to more closely match stock EL tomcat package
* Mon Jul 1 2013 Nathan Milford <nathan@milford.io>
- 7.0.41
