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

%package -n     python3-%{pname}
Summary:        Oslo service library
%{?python_provide:%python_provide python3-%{pname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  git
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-eventlet
BuildRequires:  python3-six
# Required for documentation build
BuildRequires:  python3-oslo-config
# Required for tests
BuildRequires:  procps-ng
BuildRequires:  python3-fixtures
BuildRequires:  python3-hacking
BuildRequires:  python3-mock
BuildRequires:  python3-requests
BuildRequires:  python3-routes
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-yappi
BuildRequires:  python3-webob
BuildRequires:  python3-paste
BuildRequires:  python3-paste-deploy

Requires:       python3-eventlet >= 0.22.0
Requires:       python3-greenlet
Requires:       python3-oslo-config >= 2:5.1.0
Requires:       python3-oslo-concurrency >= 3.25.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.40.2
Requires:       python3-routes
Requires:       python3-six >= 1.10.0
Requires:       python3-yappi
Requires:       python3-debtcollector
Requires:       python3-webob
Requires:       python3-paste
Requires:       python3-paste-deploy >= 1.5.0


%description -n python3-%{pname}
%{common_desc}

%package -n python3-%{pname}-tests
Summary:        Oslo service tests
%{?python_provide:%python_provide python3-%{pname}-tests}

Requires:  python3-%{pname} = %{version}-%{release}
Requires:  procps-ng
Requires:  python3-fixtures
Requires:  python3-hacking
Requires:  python3-mock
Requires:  python3-requests
Requires:  python3-routes
Requires:  python3-oslotest

%description -n python3-%{pname}-tests
%{common_desc1}

%if 0%{?with_doc}
%package -n python-%{pname}-doc
Summary:        Oslo service documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python-%{pname}-doc
Documentation for oslo.service
%endif

%description
%{common_desc}

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
python3 setup.py build_sphinx -b html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%{py3_install}

%check
# FIXME: https://review.openstack.org/279011 seems to break tests in CentOS7,
# creating an infinite loop
#python3 setup.py test ||
#rm -rf .testrepository

%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_service
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_service/tests

%files -n python3-%{pname}-tests
%{python3_sitelib}/oslo_service/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
