%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.service
%global pname oslo-service

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name:           python-%{pname}
Version:        1.25.1
Release:        1%{?dist}
Summary:        Oslo service library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%package -n     python2-%{pname}
Summary:        Oslo service library
%{?python_provide:%python_provide python2-%{pname}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  git
BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-oslo-i18n
BuildRequires:  python-paste
BuildRequires:  python-paste-deploy
BuildRequires:  python-eventlet
BuildRequires:  python-monotonic
BuildRequires:  python-six
# Required for documentation build
BuildRequires:  python-oslo-config
# Required for tests
BuildRequires:  procps-ng
BuildRequires:  python-fixtures
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-requests
BuildRequires:  python-routes
BuildRequires:  python-oslotest
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-webob

Requires:       python-eventlet >= 0.18.2
Requires:       python-greenlet
Requires:       python-monotonic >= 0.6
Requires:       python-oslo-config >= 2:4.0.0
Requires:       python-oslo-concurrency >= 3.8.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.22.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-paste
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-routes
Requires:       python-six >= 1.9.0
Requires:       python-webob


%description -n python2-%{pname}
Library for running OpenStack services

%package -n python2-%{pname}-tests
Summary:        Oslo service tests
%{?python_provide:%python_provide python2-%{pname}-tests}

Requires:  python-%{pname} = %{version}-%{release}
Requires:  procps-ng
Requires:  python-fixtures
Requires:  python-hacking
Requires:  python-mock
Requires:  python-requests
Requires:  python-routes
Requires:  python-oslotest

%description -n python2-%{pname}-tests
Tests for oslo.service


%if 0%{?with_python3}
%package -n     python3-%{pname}
Summary:        Oslo service library
%{?python_provide:%python_provide python3-%{pname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 2.0.0
# Required for tests
BuildRequires:  procps-ng
BuildRequires:  python3-fixtures
BuildRequires:  python3-hacking
BuildRequires:  python3-mock
BuildRequires:  python3-requests
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-concurrency

Requires:       python3-eventlet >= 0.18.2
Requires:       python3-greenlet
Requires:       python3-monotonic >= 0.6
Requires:       python3-oslo-config >= 2:4.0.0
Requires:       python3-oslo-concurrency >= 3.8.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-log >= 3.22.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-paste
Requires:       python3-paste-deploy >= 1.5.0
Requires:       python3-routes
Requires:       python3-six >= 1.9.0
Requires:       python3-webob


%description -n python3-%{pname}
Library for running OpenStack services

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
Tests for oslo.service
%endif


%package -n python-%{pname}-doc
Summary:        Oslo service documentation
%description -n python-%{pname}-doc
Documentation for oslo.service

%description
Library for running OpenStack services

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
%if 0%{?with_python3}
%{__python3} setup.py test ||
rm -rf .testrepository
%endif
# FIXME: https://review.openstack.org/279011 seems to break tests in CentOS7,
# creating an infinite loop
#%{__python2} setup.py test ||

%files -n python2-%{pname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_service
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_service/tests

%files -n python2-%{pname}-tests
%{python2_sitelib}/oslo_service/tests

%if 0%{?with_python3}
%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_service
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_service/tests

%files -n python3-%{pname}-tests
%{python3_sitelib}/oslo_service/tests
%endif

%files -n python-%{pname}-doc
%doc doc/build/html
%license LICENSE

%changelog
* Tue Nov 21 2017 RDO <dev@lists.rdoproject.org> 1.25.1-1
- Update to 1.25.1

* Fri Aug 11 2017 Alfredo Moralejo <amoralej@redhat.com> 1.25.0-1
- Update to 1.25.0

