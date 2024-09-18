#!/bin/sh

BASEDIR="`dirname "$0"`"
case "$BASEDIR" in
	/*)
		# Absolute path
		true
		;;
	*)
		# Relative path
		BASEDIR="${PWD}/${BASEDIR}"
		;;
esac

rpmdev-setuptree
cd "${BASEDIR}"
tomcat_version="`grep -F Version tomcat8.spec | sed 's/^[^ ]* *//'`"
cp tomcat8.spec "${HOME}"/rpmbuild/SPECS
cp tomcat8.init tomcat8.sysconfig tomcat8.logrotate "${HOME}"/rpmbuild/SOURCES
# wget -P "${HOME}"/rpmbuild/SOURCES https://archive.apache.org/dist/tomcat/tomcat-7/v${tomcat_version}/bin/apache-tomcat-${tomcat_version}.tar.gz
( cd "${HOME}"/rpmbuild/SOURCES && curl -O "https://archive.apache.org/dist/tomcat/tomcat-8/v${tomcat_version}/bin/apache-tomcat-${tomcat_version}.tar.gz" )
rpmbuild -bb "${HOME}"/rpmbuild/SPECS/tomcat8.spec
