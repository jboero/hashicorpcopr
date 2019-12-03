# https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Name:		terraform
Version:	0.12.17
Release:	1
Summary:	Hashicorp terraform provisioning tool.
License:	MPL
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Requires(pre):	shadow-utils
Requires(post):	systemd libcap
URL:		https://www.%{name}.io/

%define debug_package %{nil}

%description
Terraform provisions multicloud resources using a common language of HCL.

%prep
%autosetup -c %{name}-%{version}

%build

%install

mkdir -p %{buildroot}%{_bindir}/
cp -p %{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}

%pre

%post

%preun

%postun

%changelog
