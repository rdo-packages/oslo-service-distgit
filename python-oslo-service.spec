%global pypi_name oslo.service

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-oslo-service
Version:        0.6.0
Release:        1%{?dist}
Summary:        Oslo service library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-monotonic


Requires:       python-babel
Requires:       python-eventlet >= 0.17.3
Requires:       python-monotonic >= 0.1
Requires:       python-oslo-config >= 1.11.0
Requires:       python-oslo-i18n
Requires:       python-oslo-utils >= 1.6.0
Requires:       python-six >= 1.9.0

%description
Library for running OpenStack services


%prep
%setup -q -n %{pypi_name}-%{upstream_version}


%build
%{__python2} setup.py build

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc html README.rst
%license LICENSE
%{python2_sitelib}/oslo_service
%{python2_sitelib}/*.egg-info

%changelog
* Tue Aug 18 2015 Alan Pevec <alan.pevec@redhat.com> 0.6.0-1
- Update to upstream 0.6.0

* Mon Jul 06 2015 Alan Pevec <alan.pevec@redhat.com> 0.3.0-1
- Update to upstream 0.3.0
