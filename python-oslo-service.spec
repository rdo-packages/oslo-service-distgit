# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.service
%global pname oslo-service
%global with_doc 1

%global common_desc \
Library for running OpenStack services

%global common_desc1 \
Tests for oslo.service

Name:           python-%{pname}
Version:        XXX
Release:        XXX
Summary:        Oslo service library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%package -n     python%{pyver}-%{pname}
Summary:        Oslo service library
%{?python_provide:%python_provide python%{pyver}-%{pname}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  git
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-six
# Required for documentation build
BuildRequires:  python%{pyver}-oslo-config
# Required for tests
BuildRequires:  procps-ng
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-routes
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-oslo-concurrency
BuildRequires:  python%{pyver}-yappi
%if %{pyver} == 2
BuildRequires:  python-paste
BuildRequires:  python-paste-deploy
BuildRequires:  python-monotonic
BuildRequires:  python-webob
%else
BuildRequires:  python%{pyver}-paste
BuildRequires:  python%{pyver}-paste-deploy
BuildRequires:  python%{pyver}-monotonic
BuildRequires:  python%{pyver}-webob
%endif

Requires:       python%{pyver}-eventlet >= 0.18.2
Requires:       python%{pyver}-greenlet
Requires:       python%{pyver}-oslo-config >= 2:5.1.0
Requires:       python%{pyver}-oslo-concurrency >= 3.25.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-utils >= 3.40.2
Requires:       python%{pyver}-routes
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-yappi
Requires:       python%{pyver}-debtcollector
%if %{pyver} == 2
Requires:       python-paste
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-monotonic >= 0.6
Requires:       python-webob
%else
Requires:       python%{pyver}-paste
Requires:       python%{pyver}-paste-deploy >= 1.5.0
Requires:       python%{pyver}-monotonic >= 0.6
Requires:       python%{pyver}-webob
%endif


%description -n python%{pyver}-%{pname}
%{common_desc}

%package -n python%{pyver}-%{pname}-tests
Summary:        Oslo service tests
%{?python_provide:%python_provide python%{pyver}-%{pname}-tests}

Requires:  python%{pyver}-%{pname} = %{version}-%{release}
Requires:  procps-ng
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-requests
Requires:  python%{pyver}-routes
Requires:  python%{pyver}-oslotest

%description -n python%{pyver}-%{pname}-tests
%{common_desc1}

%if 0%{?with_doc}
%package -n python%{pyver}-%{pname}-doc
Summary:        Oslo service documentation
%{?python_provide:%python_provide python%{pyver}-%{pname}-doc}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python%{pyver}-%{pname}-doc
Documentation for oslo.service
%endif

%description
%{common_desc}

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%{pyver_install}

%check
# FIXME: https://review.openstack.org/279011 seems to break tests in CentOS7,
# creating an infinite loop
#%{pyver_bin} setup.py test ||
#rm -rf .testrepository

%files -n python%{pyver}-%{pname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/oslo_service
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_service/tests

%files -n python%{pyver}-%{pname}-tests
%{pyver_sitelib}/oslo_service/tests

%if 0%{?with_doc}
%files -n python%{pyver}-%{pname}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
