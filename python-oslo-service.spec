%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

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

License:        Apache-2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n     python3-%{pname}
Summary:        Oslo service library

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
BuildRequires:  procps-ng

%description -n python3-%{pname}
%{common_desc}

%package -n python3-%{pname}-tests
Summary:        Oslo service tests

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

%description -n python-%{pname}-doc
Documentation for oslo.service
%endif

%description
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

# We have to generate documentation after install phase because sphinx-build
# needs .dist-info directory to be available in order to build successfully.
%if 0%{?with_doc}
# generate html docs
PYTHONPATH="%{buildroot}/%{python3_sitelib}"
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%check
%tox -e %{default_toxenv}

%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_service
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/oslo_service/tests

%files -n python3-%{pname}-tests
%{python3_sitelib}/oslo_service/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
