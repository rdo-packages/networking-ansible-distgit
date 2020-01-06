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
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global library networking-ansible
%global module networking_ansible
%global ansible_role openstack-ml2

Name:       python-%{library}
Version:    3.0.0
Release:    1%{?dist}
Summary:    OpenStack Neutron ML2 driver for Ansible Networking
License:    ASL 2.0
URL:        https://storyboard.openstack.org/#!/project/986

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python%{pyver}-%{library}
Summary:   OpenStack Neutron ML2 driver for Ansible Networking
%{?python_provide:%python_provide python%{pyver}-%{library}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-neutron-lib
# Required to compile translation files (add only if exist)
BuildRequires:  python%{pyver}-babel

Requires:  python%{pyver}-oslo-config >= 2:5.2.0
Requires:  python%{pyver}-pbr >= 2.0
Requires:  python%{pyver}-neutron-lib >= 1.18.0
Requires:  openstack-neutron-common >= 1:13.0.0
Requires:  python%{pyver}-ansible-runner >= 1.0.5
Requires:  python%{pyver}-network-runner

# Python code cannot work without the ansible roles
Requires:  ansible-role-%{ansible_role} = %{version}-%{release}

%description -n python%{pyver}-%{library}
OpenStack Neutron ML2 driver for Ansible Networking


%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack Neutron ML2 driver for Ansible Networking tests
Requires:   python%{pyver}-%{library} = %{version}-%{release}
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-neutron
BuildRequires:  python%{pyver}-neutron-tests
BuildRequires:  python%{pyver}-neutron-lib-tests
BuildRequires:  python%{pyver}-tempest
BuildRequires:  python%{pyver}-ansible-runner
BuildRequires:  python%{pyver}-network-runner


Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest >= 1.10.0
Requires:  python%{pyver}-subunit >= 1.0.0
Requires:  python%{pyver}-stestr

%description -n python%{pyver}-%{library}-tests
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible test files.

%if 0%{?with_doc}
%package -n python%{pyver}-%{library}-doc
Summary:    OpenStack Neutron ML2 driver for Ansible Networking Documentaion
%{?python_provide:%python_provide python%{pyver}-%{library}-doc}

BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx

%description -n python%{pyver}-%{library}-doc
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible documentation.
%endif

%description
OpenStack Neutron ML2 driver for Ansible Networking


%package -n ansible-role-%{ansible_role}
Summary:   Role for OpenStack ML2 ansible mechanism driver

%description -n ansible-role-%{ansible_role}
Ansible roles for OpenStack ML2 mechanism driver


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourselves
%{py_req_cleanup}

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Remove config sample and .travis file
rm -rf %{buildroot}/usr/etc/neutron %{buildroot}/usr/etc/ansible/roles/%{ansible_role}/.travis.yml

# Move openstack-ml2 role to proper location
install -d -m 755 %{buildroot}%{_datadir}/ansible/roles
mv %{buildroot}/usr/etc/ansible/roles/%{ansible_role} %{buildroot}%{_datadir}/ansible/roles

%check
PYTHON=%{pyver_bin} stestr-%{pyver} run

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python%{pyver}-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%files -n ansible-role-%{ansible_role}
%license LICENSE
%{_datadir}/ansible/roles/%{ansible_role}/*

%changelog
* Thu Oct 31 2019 Alfredo Moralejo <amoralej@redhat.com> 3.0.0-1
- Update to 3.0.0

* Thu Oct 24 2019 Yatin Karel <ykarel@redhat.com> 1.1.1-0.1.5cefa6agit
- Update to pre release 1.1.1 (5cefa6a7c6ee3ec2c25e23f25bdae9138202513e)
