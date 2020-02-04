# https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Name:		consul
#Version:	1.6.2+ent
Version:	1.6.3
Release:	2%{?dist}
Summary:	Consul is a tool for service discovery
License:	MPL
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}-server.hcl
Source2:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.service
Source3:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}-agent.hcl
BuildRequires:  systemd coreutils unzip
Requires(pre):	shadow-utils
Requires(post):	systemd libcap
Requires(preun):	systemd
Requires(postun):	systemd
URL:		https://www.consul.io/

%define debug_package %{nil}

%description
Consul secures, stores, and tightly controls access to tokens, passwords,
certificates, API keys, and other secrets in modern computing. Consul handles
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

mkdir -p %{buildroot}%{_sysconfdir}/%{name}.d
cp -p %{SOURCE1} %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}.d/

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# Remember some releases don't use _unitdir..
mkdir -p %{buildroot}/usr/lib/systemd/system
cp -p %{SOURCE2} %{buildroot}/usr/lib/systemd/system/

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}.d/%{name}-server.hcl
%config(noreplace) %{_sysconfdir}/%{name}.d/%{name}-agent.hcl
%attr(0750,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
/usr/lib/systemd/system/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
    useradd -r -d %{_sharedstatedir}/%{name} -g %{name} \
    -s /sbin/nologin -c "Consul secret management tool" %{name}
exit 0

%post
%systemd_post %{name}.service
/sbin/setcap cap_ipc_lock=+ep %{_bindir}/%{name}

%preun
%systemd_preun %{name}.service
if [ $1 -eq 0 ]; then
      /usr/bin/systemctl --no-reload disable %{name}.service
      /usr/bin/systemctl stop %{name}.service >/dev/null 2>&1 ||:
      /usr/bin/systemctl disable %{name}.service

    fi
    if [ $1 -eq 1 ]; then
      /usr/bin/systemctl --no-reload disable %{name}.service
      /usr/bin/systemctl stop %{name}.service
    fi

%postun
%systemd_postun_with_restart %{name}.service

%changelog
