# https://fedoraproject.org/wiki/How_to_create_an_RPM_package
# Built and maintained by John Boero - jboero@hashicorp.com
# In honor of Seth Vidal https://www.redhat.com/it/blog/thank-you-seth-vidal

%define hashiarch %(if [ "%{_arch}" == 'x86_64' ]; then echo 'amd64'; elif [ "%{_arch}" == 'aarch64' ]; then echo 'arm64'; elif [ "%_arch" == 'i386' ]; then echo '386'; else echo "%{_arch}"; fi)

Name:		consul-k8s
Version:	0.35.0
Release:	1%{?dist}
Summary:	Consul-K8s is a tool for service discovery and Kubernetes
License:	MPL
Source0:	https://github.com/hashicorp/%{name}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:  systemd coreutils unzip upx golang-bin
Requires(pre):	shadow-utils
Requires(post):	systemd libcap
Requires(preun):	
Requires(postun):	
URL:		https://www.consul.io/

%define debug_package %{nil}

%description
Consul service discovery with Kubernetes.

%prep
%autosetup -c %{name}-%{version}

%build
pwd
ls
cd %{_builddir}/cli/

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
