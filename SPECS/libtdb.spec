%global package_speccommit ba30736e9fe9619a10292c1bdad6b2ba7dbc440e
%global usver 1.4.14
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}

Name: libtdb
Version: 1.4.14
Release: %{?xsrel}.1%{?dist}
Summary:         The tdb library
License:         LGPL-3.0-or-later
URL:             http://tdb.samba.org/
Source0: tdb-1.4.14.tar.gz
Patch0: CA-420336-tdbtool-fix-parse_hex.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: gnupg2
BuildRequires: python3-devel

Provides: bundled(libreplace)

# Python bindings no more used by system:
# Samba does not build runtime python libraries anymore
# XS removal of a version XCP-ng did not ship
Obsoletes: python2-tdb < 1.4.2-1
# XCP-ng: Removal of a previous samba requirement
Obsoletes: python-tdb <= 1.3.18-1.el7

%description
A library that implements a trivial database.

%package         devel
Summary:         Header files need to link the Tdb library

Requires: libtdb = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Tdb library.

%package -n tdb-tools
Summary:         Developer tools for the Tdb library

Requires: libtdb = %{version}-%{release}

%description -n tdb-tools
Tools to manage Tdb files

%package -n python3-tdb
Summary: Python3 bindings for the Tdb library
Requires: libtdb = %{version}-%{release}
%{?python_provide:%python_provide python3-tdb}

%description -n python3-tdb
Python3 bindings for libtdb

%prep
%autosetup -n tdb-%{version} -p1

%build
# workaround https://gitlab.com/ita1024/waf/-/issues/2472
export PYTHONARCHDIR=%{python3_sitearch}
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

%make_build

%check
%make_build check

%install
%make_install

%files
%license LICENSE
%{_libdir}/libtdb.so.*

%files devel
%doc docs/README
%{_includedir}/tdb.h
%{_libdir}/libtdb.so
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-tools
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbrestore

%files -n python3-tdb
%{python3_sitearch}/__pycache__/_tdb_text.cpython*.py[co]
%{python3_sitearch}/tdb.cpython*.so
%{python3_sitearch}/_tdb_text.py

%ldconfig_scriptlets

%changelog
* Wed Jul 08 2026 Philippe Coval <philippe.coval@vates.tech> - 1.4.14-1.1
- Obsolete python-tdb (no more needed by system, samba)

* Mon Sep 22 2025 Lin Liu <Lin.Liu01@cloud.com> - 1.4.14-1
- CP-310101: Update with samba

* Tue Jan 21 2025 XenServer Rebuild <rebuild@xenserver.com> - 1.4.8-2
- CP-53310: XenServer 9 rebuild

* Thu Dec 14 2023 Lin Liu <lin.liu@citrix.com> - 1.4.8-1
- Update to 1.4.8

* Wed Jul 05 2023 Lin Liu <lin.liu@citrix.com> - 1.4.7-1
- First imported release

