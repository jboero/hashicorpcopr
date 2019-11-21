# https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Name:		nomad
Version:	0.10.1
Release:	1%{?dist}
Summary:	Hashicorp Nomad job scheduler
License:	Hashicorp
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.hcl
Source2:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.agent.hcl
Source3:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.service
Requires(pre):	shadow-utils
Requires(post):	systemd libcap
#Requires(preun):	systemd
#Requires(postun):	systemd
URL:		https://www.nomadproject.io/

%define debug_package %{nil}

%description
nomad secures, stores, and tightly controls access to tokens, passwords,
certificates, API keys, and other secrets in modern computing. nomad handles
leasing, key revocation, key rolling, and auditing. Through a unified API, users
can access an encrypted Key/Value store and network encryption-as-a-service, or
generate AWS IAM/STS credentials, SQL/NoSQL databases, X.509 certificates, SSH
credentials, and more.

%prep
%autosetup -c %{name}-%{version}

%build

%install

mkdir -p %{buildroot}%{_bindir}/
cp -p %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}.hcl
cp -p %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.agent.hcl

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/plugins

# Some platforms don't have unitdir... ugh
mkdir -p %{buildroot}/usr/lib/systemd/system
cp -p %{SOURCE3} %{buildroot}/usr/lib/systemd/system/

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.hcl
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.agent.hcl
%attr(0750,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
/usr/lib/systemd/system/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
    useradd -r -d %{_sharedstatedir}/%{name} -g %{name} \
    -s /sbin/nologin -c "Hashicorp Nomad job scheduler" %{name}
exit 0

%post
%systemd_post %{name}.service
/sbin/setcap cap_ipc_lock=+ep %{_bindir}/%{name}

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
