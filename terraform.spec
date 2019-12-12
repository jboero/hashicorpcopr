# https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Name:		terraform
Version:	0.12.18
Release:	1%{?dist}
Summary:	Hashicorp terraform provisioning tool.
License:	MPL
# Our engineering uses "amd64" instead of "x86_64" so ugly ugly sedification...
Source0:	'https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_%(echo "%{_arch}" | sed -e "s/amd64/x86_64/").zip'
# Some builds fail on systemd, but hey, systemd right? 👍
BuildRequires: (systemd or bash)
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
