%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library networking-ansible
%global module networking_ansible

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Neutron ML2 driver for Ansible Networking
License:    ASL 2.0
URL:        https://storyboard.openstack.org/#!/project/986

Source0:    http://tarballs.openstack.org/%{library}/%{library}-master.tar.gz

BuildArch:  noarch
BuildRequires:  git

%package -n python2-%{library}
Summary:    penStack Neutron ML2 driver for Ansible Networking
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

%description -n python2-%{library}
OpenStack Neutron ML2 driver for Ansible Networking


%package -n python2-%{library}-tests
Summary:    OpenStack Neutron ML2 driver for Ansible Networking tests
Requires:   python2-%{library} = %{version}-%{release}
BuildRequires: python2-mock
BuildRequires: python2-oslo-config


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
Requires:  python-neutron


%description -n python3-%{library}
OpenStack Neutron ML2 driver for Ansible Networking


%package -n python3-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python3-%{library} = %{version}-%{release}
BuildRequires: python3-mock
BuildRequires: python3-oslo-config

%description -n python3-%{library}-tests
OpenStack Neutron ML2 driver for Ansible Networking

This package contains the networking-ansible test files.

%endif # with_python3


%description
OpenStack Neutron ML2 driver for Ansible Networking


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

%changelog
* Tue May 15 2018 Dan Radez <dradez@redhat.com> - 0.0.1-1
- Initial package.
