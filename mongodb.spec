Name: mongodb
Version: 2.0.5
Release: 1%{?dist}
Summary: mongo client shell and tools
License: AGPL 3.0
URL: http://www.mongodb.org
Group: Applications/Databases

Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: js-devel, readline-devel, boost-devel, pcre-devel
BuildRequires: gcc-c++, scons

%description
Mongo (from "huMONGOus") is a schema-free document-oriented database.
It features dynamic profileable queries, full indexing, replication
and fail-over support, efficient storage of large binary data objects,
and auto-sharding.

This package provides the mongo shell, import/export tools, and other
client utilities.


#### Router
%package router
Summary: mongo server, sharding server, and support scripts
Group: Applications/Databases
Requires: mongodb

%description router
Mongo (from "huMONGOus") is a schema-free document-oriented database.

This package provides the mongo server software, mongo sharding server
softwware, default configuration files, and init.d scripts.


#### Shard #########
%package shard
Summary: mongo shard, sharding server, and support scripts
Group: Applications/Databases
Requires: mongodb

%description shard
Mongo (from "huMONGOus") is a schema-free document-oriented database.

This package provides the mongo server sharding software, mongo sharding server
software, default configuration files, and init.d scripts.

#### Config ########
%package config
Summary: Headers and libraries for mongo development. 
Group: Applications/Databases
Requires: mongodb

%description config
Mongo (from "huMONGOus") is a schema-free document-oriented database.

This package provides the mongo static library and header files needed
to develop mongo client software.


%prep
%setup

%build
scons --prefix=$RPM_BUILD_ROOT/usr all
# XXX really should have shared library here

%install
scons --prefix=$RPM_BUILD_ROOT/usr install
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
cp debian/*.1 $RPM_BUILD_ROOT/usr/share/man/man1/
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
#cp rpm/init.d-mongod $RPM_BUILD_ROOT/etc/rc.d/init.d/mongod
#chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongod
mkdir -p $RPM_BUILD_ROOT/etc
#cp rpm/mongod.conf $RPM_BUILD_ROOT/etc/mongod.conf
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
#cp rpm/mongod.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/mongod
#mkdir -p $RPM_BUILD_ROOT/var/lib/mongo
mkdir -p $RPM_BUILD_ROOT/var/log/mongo
#touch $RPM_BUILD_ROOT/var/log/mongo/mongod.log

#%install router
cp /root/rpmbuild/SOURCES/mongodb/etc/rc.d/init.d/mongor $RPM_BUILD_ROOT/etc/rc.d/init.d/mongor
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongor
cp /root/rpmbuild/SOURCES/mongodb/etc/sysconfig/mongor $RPM_BUILD_ROOT/etc/sysconfig/mongor
cp /root/rpmbuild/SOURCES/mongodb/etc/mongor.conf $RPM_BUILD_ROOT/etc/mongor.conf
touch $RPM_BUILD_ROOT/var/log/mongo/mongor.log


#%install shard
cp /root/rpmbuild/SOURCES/mongodb/etc/rc.d/init.d/mongos $RPM_BUILD_ROOT/etc/rc.d/init.d/mongos
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongos
cp /root/rpmbuild/SOURCES/mongodb/etc/sysconfig/mongos $RPM_BUILD_ROOT/etc/sysconfig/mongos
cp /root/rpmbuild/SOURCES/mongodb/etc/mongos.conf $RPM_BUILD_ROOT/etc/mongos.conf
touch $RPM_BUILD_ROOT/var/log/mongo/mongos.log
mkdir -p $RPM_BUILD_ROOT/data/db/


#%install config
cp /root/rpmbuild/SOURCES/mongodb/etc/rc.d/init.d/mongoc $RPM_BUILD_ROOT/etc/rc.d/init.d/mongoc
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongoc
cp /root/rpmbuild/SOURCES/mongodb/etc/sysconfig/mongoc $RPM_BUILD_ROOT/etc/sysconfig/mongoc
cp /root/rpmbuild/SOURCES/mongodb/etc/mongoc.conf $RPM_BUILD_ROOT/etc/mongoc.conf
touch $RPM_BUILD_ROOT/var/log/mongo/mongoc.log
mkdir -p $RPM_BUILD_ROOT/data/configdb

%clean
scons -c
rm -rf $RPM_BUILD_ROOT




#### All
%pre
if ! /usr/bin/id -g mongod &>/dev/null; then
    /usr/sbin/groupadd -r mongod
fi
if ! /usr/bin/id mongod &>/dev/null; then
    /usr/sbin/useradd -M -r -g mongod -d /var/lib/mongo -s /bin/false \
	-c mongod mongod > /dev/null 2>&1
fi

#############################
#### Router

%post router
if test $1 = 1
then
  /sbin/chkconfig --add mongor
fi

%preun router
if test $1 = 0
then
  /sbin/chkconfig --del mongor
fi

%postun router
if test $1 -ge 1
then
  /sbin/service mongor condrestart >/dev/null 2>&1 || :
fi

#############################
#### Shard

%post shard
if test $1 = 1
then
  /sbin/chkconfig --add mongos
fi

%preun shard
if test $1 = 0
then
  /sbin/chkconfig --del mongos
fi

%postun shard
if test $1 -ge 1
then
  /sbin/service mongos condrestart >/dev/null 2>&1 || :
fi

#############################
#### Config

%post config
if test $1 = 1
then
  /sbin/chkconfig --add mongoc
fi

%preun config
if test $1 = 0
then
  /sbin/chkconfig --del mongoc
fi

%postun config
if test $1 -ge 1
then
  /sbin/service mongoc condrestart >/dev/null 2>&1 || :
fi







%files
%defattr(-,root,root,-)
%doc README GNU-AGPL-3.0.txt

%{_bindir}/mongo
%{_bindir}/mongodump
%{_bindir}/mongoexport
%{_bindir}/mongofiles
%{_bindir}/mongoimport
%{_bindir}/mongorestore
%{_bindir}/mongostat
%{_bindir}/bsondump
%{_bindir}/mongotop
%{_bindir}/mongod
%{_bindir}/mongos

%{_mandir}/man1/mongo.1*
%{_mandir}/man1/mongod.1*
%{_mandir}/man1/mongodump.1*
%{_mandir}/man1/mongoexport.1*
%{_mandir}/man1/mongofiles.1*
%{_mandir}/man1/mongoimport.1*
%{_mandir}/man1/mongosniff.1*
%{_mandir}/man1/mongostat.1*
%{_mandir}/man1/mongorestore.1*
%{_mandir}/man1/bsondump.1*
%{_mandir}/man1/mongos.1*

%attr(0755,mongod,mongod) %dir /var/log/mongo


%files router
%defattr(-,root,root,-)
%config(noreplace) /etc/mongor.conf
/etc/rc.d/init.d/mongor
/etc/sysconfig/mongor
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongo/mongor.log


%files shard
%defattr(-,root,root,-)
%config(noreplace) /etc/mongos.conf
/etc/rc.d/init.d/mongos
/etc/sysconfig/mongos
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongo/mongos.log


%files config
%defattr(-,root,root,-)
%config(noreplace) /etc/mongoc.conf
/etc/rc.d/init.d/mongoc
/etc/sysconfig/mongoc
%attr(0755,mongod,mongod) %dir /data/db
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongo/mongoc.log


%changelog
* Mon Jan 16 2012 Martin Lazarov <martin@lazarov.bg>
- removed devel & server packages and added router, shard and config packages

* Thu Jan 28 2010 Richard M Kreuter <richard@10gen.com>
- Minor fixes.

* Sat Oct 24 2009 Joe Miklojcik <jmiklojcik@shopwiki.com> - 
- Wrote mongo.spec.
