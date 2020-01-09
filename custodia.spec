%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora}
%global with_python3 1
%global with_tox 1
%endif

Name:           custodia
Version:        0.1.0
Release:        4%{?dist}
Summary:        A service to manage, retrieve and store secrets for other processes.

License:        GPLv3+
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/custodia-%{version}.tar.gz
Source1:        https://github.com/latchset/%{name}/releases/download/v%{version}/custodia-%{version}.tar.gz.sha512sum.txt

BuildArch:      noarch

BuildRequires:      python-devel
BuildRequires:      python-setuptools
BuildRequires:      python-jwcrypto
%if 0%{?with_tox}
BuildRequires:      python-tox
BuildRequires:      python-coverage
%endif
BuildRequires:      pytest
Requires:           python-jwcrypto
Requires:           python-custodia

%if 0%{?with_python3}
BuildRequires:      python3-devel
BuildRequires:      python3-setuptools
BuildRequires:      python3-jwcrypto
BuildRequires:      python3-pytest
%if 0%{?with_tox}
BuildRequires:      python3-tox
BuildRequires:      python3-coverage
%endif
%endif

%if 0%{?with_tox}
Patch01: 0001-Allow-tox-to-use-locally-installed-packages.patch
%endif
Patch02: 0002-Use-OAEP-instead-of-PKCS1v15.patch

%description
A service to manage, retrieve and store secrets for other processes.

%package -n python-custodia
Summary:    Subpackage with python custodia modules
Requires:   python-jwcrypto

%description -n python-custodia
Subpackage with python custodia modules

%if 0%{?with_python3}
%package -n python3-custodia
Summary:    Subpackage with python3 custodia modules
Requires:   python3-jwcrypto

%description -n python3-custodia
Subpackage with python custodia modules
%endif

%prep
grep `sha512sum %{SOURCE0}` %{SOURCE1} || (echo "Checksum invalid!" && exit 1)
%setup
%patch02 -p1

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}/usr/share/doc/custodia _doc_staging
rm -rf %{buildroot}%{python2_sitelib}/tests
rm -rf %{buildroot}%{python2_sitelib}/__pycache__
mkdir -p %{buildroot}/%{_sbindir}
mv %{buildroot}/%{_bindir}/custodia %{buildroot}/%{_sbindir}/custodia
%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}/usr/share/doc/custodia
rm -rf %{buildroot}%{python3_sitelib}/tests
rm -rf %{buildroot}%{python3_sitelib}/__pycache__
rm -rf %{buildroot}/%{_bindir}/custodia
%endif


%check
mkdir docs/source/_static
%if 0%{?with_tox}
tox -e py27
%if 0%{?with_python3}
tox -e py34
%endif
%else
# tests are failing on build machines
# %{__python2} -m py.test ./tests/tests.py
%endif  # with_tox


%files
%doc README API.md _doc_staging/*
%license LICENSE
%{_mandir}/man7/custodia*
%{_sbindir}/custodia

%files -n python-custodia
%license LICENSE
%{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-custodia
%license LICENSE
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-*.egg-info
%endif


%changelog
* Wed Sep 07 2016 Christian Heimes <cheimes@redhat.com> - 0.1.0-4
- Disable tests (broken on build machines)
- related: #1371902

* Wed Sep 07 2016 Simo Sorce <simo@redhat.com> - 0.1.0-3
- Change default to use RSA OAEP padding
- resolves: #1371902

* Mon Apr 04 2016 Christian Heimes <cheimes@redhat.com> - 0.2.1-2
- Correct download link

* Thu Mar 31 2016 Christian Heimes <cheimes@redhat.com> - 0.1.0-1
- Initial packaging
