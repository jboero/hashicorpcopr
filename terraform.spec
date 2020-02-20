# https://fedoraproject.org/wiki/How_to_create_an_RPM_package
# Can't escape ) in macro sadly so no case...
%define hashiarch %(if [ "%{_arch}" == 'x86_64' ]; then echo 'amd64'; elif [ "%{_arch}" == 'aarch64' ]; then echo 'arm'; elif [ "%_arch" == 'i386' ]; then echo '386'; else echo "%{_arch}"; fi)

Name:           terraform
Version:        0.12.21
Release:        1%{?dist}
Summary:        Hashicorp terraform provisioning tool.
License:        MPL
# Our engineering uses "amd64" instead of "x86_64" so ugly mapping...
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_%{hashiarch}.zip
Source1:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_arm.zip
Source2:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_386.zip

# Some builds fail on systemd, but hey, systemd right? 👍
BuildRequires: systemd unzip
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
