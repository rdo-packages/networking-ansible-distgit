%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library networking-ansible
%global module networking_ansible
%global ansible_role openstack-ml2

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Neutron ML2 driver for Ansible Networking
License:    ASL 2.0
URL:        https://storyboard.openstack.org/#!/project/986

Source0:    http://tarballs.openstack.org/%{library}/%{library}-master.tar.gz

BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python2-%{library}
Summary:   OpenStack Neutron ML2 driver for Ansible Networking
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-neutron-lib
# Required to compile translation files (add only if exist)
BuildRequires:  python2-babel

Requires:  python2-oslo-config >= 2:5.1.0
Requires:  python2-pbr
Requires:  python2-neutron-lib
Requires:  python-neutron
Requires:  python2-ansible-runner

# Python code cannot work without the ansible roles
Requires:  ansible-role-%{ansible_role} = %{version}-%{release}

%description -n python2-%{library}
OpenStack Neutron ML2 driver for Ansible Networking


%package -n python2-%{library}-tests
Summary:    OpenStack Neutron ML2 driver for Ansible Networking tests
Requires:   python2-%{library} = %{version}-%{release}
BuildRequires:  python2-mock
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslotest
BuildRequires:  python2-stestr
BuildRequires:  python2-subunit
BuildRequires:  python-neutron
BuildRequires:  python-neutron-tests
BuildRequires:  python2-neutron-lib-tests
BuildRequires:  python2-tempest


Requires:  python2-mock
Requires:  python2-oslotest >= 1.10.0
Requires:  python2-subunit >= 1.0.0
Requires:  python2-stestr

%description -n python2-%{library}-tests
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible test files.


%package -n python-%{library}-doc
Summary:    OpenStack Neutron ML2 driver for Ansible Networking Documentaion

BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx

%description -n python-%{library}-doc
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack Neutron ML2 driver for Ansible Networking
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-neutron-lib

Requires:  python3-oslo-config >= 2:5.1.0
Requires:  python3-pbr
Requires:  python3-neutron-lib
Requires:  python3-neutron
Requires:  python3-ansible-runner

# Python code cannot work without the ansible roles
Requires:  ansible-role-%{ansible_role} = %{version}-%{release}

%description -n python3-%{library}
OpenStack Neutron ML2 driver for Ansible Networking


%package -n python3-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python3-%{library} = %{version}-%{release}
BuildRequires:  python3-mock
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-subunit
BuildRequires:  python3-neutron
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-tempest

Requires:  python2-mock
Requires:  python2-oslotest >= 1.10.0
Requires:  python2-subunit >= 1.0.0
Requires:  python2-stestr


%description -n python3-%{library}-tests
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible test files.

%endif # with_python3


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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Remove config sample and .travis file
rm -rf %{buildroot}/usr/etc/neutron %{buildroot}/usr/etc/ansible/roles/%{ansible_role}/.travis.yml

# Move openstack-ml2 role to proper location
install -d -m 755 %{buildroot}%{_datadir}/ansible/roles
mv %{buildroot}/usr/etc/ansible/roles/%{ansible_role} %{buildroot}%{_datadir}/ansible/roles

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%files -n ansible-role-%{ansible_role}
%license LICENSE
%{_datadir}/ansible/roles/%{ansible_role}/*

%changelog