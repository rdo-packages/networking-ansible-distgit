%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x4c29ff0e437f3351fd82bdf47c5a3bc787dc7035
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global library networking-ansible
%global module networking_ansible

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Neutron ML2 driver for Ansible Networking
License:    Apache-2.0
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

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

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# Remove config sample
rm -rf %{buildroot}/usr/etc/neutron

%check
%tox -e %{default_toxenv}

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.dist-info
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
