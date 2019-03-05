%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.service
%global pname oslo-service
%global with_doc 1
%if 0%{?fedora} >= 24 || 0%{?rhel} > 7
%global with_python3 1
%endif

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

%package -n     python2-%{pname}
Summary:        Oslo service library
%{?python_provide:%python_provide python2-%{pname}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr >= 2.0.0
BuildRequires:  git
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-eventlet
BuildRequires:  python2-six
# Required for documentation build
BuildRequires:  python2-oslo-config
# Required for tests
BuildRequires:  procps-ng
BuildRequires:  python2-fixtures
BuildRequires:  python2-hacking
BuildRequires:  python2-mock
BuildRequires:  python2-requests
BuildRequires:  python2-routes
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-oslo-concurrency
BuildRequires:  python2-yappi
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python2-paste
BuildRequires:  python2-paste-deploy
BuildRequires:  python2-monotonic
BuildRequires:  python2-webob
%else
BuildRequires:  python-paste
BuildRequires:  python-paste-deploy
BuildRequires:  python-monotonic
BuildRequires:  python-webob
%endif

Requires:       python2-eventlet >= 0.18.2
Requires:       python2-greenlet
Requires:       python2-oslo-config >= 2:5.1.0
Requires:       python2-oslo-concurrency >= 3.25.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-utils >= 3.40.2
Requires:       python2-routes
Requires:       python2-six >= 1.10.0
Requires:       python2-yappi
Requires:       python2-debtcollector
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python2-paste
Requires:       python2-paste-deploy >= 1.5.0
Requires:       python2-monotonic >= 0.6
Requires:       python2-webob
%else
Requires:       python-paste
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-monotonic >= 0.6
Requires:       python-webob
%endif


%description -n python2-%{pname}
%{common_desc}

%package -n python2-%{pname}-tests
Summary:        Oslo service tests
%{?python_provide:%python_provide python2-%{pname}-tests}

Requires:  python2-%{pname} = %{version}-%{release}
Requires:  procps-ng
Requires:  python2-fixtures
Requires:  python2-hacking
Requires:  python2-mock
Requires:  python2-requests
Requires:  python2-routes
Requires:  python2-oslotest

%description -n python2-%{pname}-tests
%{common_desc1}


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
BuildRequires:  python3-yappi

Requires:       python3-eventlet >= 0.18.2
Requires:       python3-greenlet
Requires:       python3-monotonic >= 0.6
Requires:       python3-oslo-config >= 2:5.1.0
Requires:       python3-oslo-concurrency >= 3.25.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.40.2
Requires:       python3-paste
Requires:       python3-paste-deploy >= 1.5.0
Requires:       python3-routes
Requires:       python3-six >= 1.10.0
Requires:       python3-webob
Requires:       python3-yappi
Requires:       python3-debtcollector


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
%endif

%if 0%{?with_doc}
%package -n python-%{pname}-doc
Summary:        Oslo service documentation

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

%description -n python-%{pname}-doc
Documentation for oslo.service
%endif

%description
%{common_desc}

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

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

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
