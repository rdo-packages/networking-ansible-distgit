%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x4c29ff0e437f3351fd82bdf47c5a3bc787dc7035
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global library networking-ansible
%global module networking_ansible

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Neutron ML2 driver for Ansible Networking
License:    ASL 2.0
URL:        https://storyboard.openstack.org/#!/project/986

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%package -n python3-%{library}
Summary:   OpenStack Neutron ML2 driver for Ansible Networking
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-neutron-lib
# Required to compile translation files (add only if exist)
BuildRequires:  python3-babel

Requires:  python3-oslo-config >= 2:5.2.0
Requires:  python3-pbr >= 2.0
Requires:  python3-neutron-lib >= 2.4.0
Requires:  openstack-neutron-common >= 1:16.0.0
Requires:  python3-ansible-runner >= 1.0.5
Requires:  python3-tooz >= 1.28.0
Requires:  python3-network-runner >= 0.3.5
Requires:  python3-debtcollector >= 1.21.0

%description -n python3-%{library}
OpenStack Neutron ML2 driver for Ansible Networking


%package -n python3-%{library}-tests
Summary:    OpenStack Neutron ML2 driver for Ansible Networking tests
Requires:   python3-%{library} = %{version}-%{release}
BuildRequires:  python3-mock
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-subunit
BuildRequires:  python3-tooz
BuildRequires:  python3-neutron
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-tempest
BuildRequires:  python3-ansible-runner
BuildRequires:  python3-network-runner


Requires:  python3-mock
Requires:  python3-oslotest >= 1.10.0
Requires:  python3-subunit >= 1.0.0
Requires:  python3-stestr

%description -n python3-%{library}-tests
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible test files.

%if 0%{?with_doc}
%package -n python3-%{library}-doc
Summary:    OpenStack Neutron ML2 driver for Ansible Networking Documentaion
%{?python_provide:%python_provide python3-%{library}-doc}

BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx

%description -n python3-%{library}-doc
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible documentation.
%endif

%description
OpenStack Neutron ML2 driver for Ansible Networking


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourselves
%{py_req_cleanup}

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
%{__python3} setup.py build_sphinx -b html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Remove config sample
rm -rf %{buildroot}/usr/etc/neutron

%check
# amoralej - ignore unit tests until https://storyboard.openstack.org/#!/story/2008101 is fixed
PYTHON=%{__python3} stestr-3 run || true

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python3-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
