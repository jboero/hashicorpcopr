# https://fedoraproject.org/wiki/How_to_create_an_RPM_package
# Built and maintained by John Boero - jboero@hashicorp.com

%define hashiarch %(if [ "%{_arch}" == 'x86_64' ]; then echo 'amd64'; elif [ "%{_arch}" == 'aarch64' ]; then echo 'arm64'; elif [ "%_arch" == 'i386' ]; then echo '386'; else echo "%{_arch}"; fi)

Name:		consul
Version:	1.7.1
Release:	1%{?dist}
Summary:	Consul is a tool for service discovery
License:	MPL
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_%{hashiarch}.zip
Source1:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}-server.json.sample
Source2:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.service
Source3:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}-agent.json
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
cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.d/
cp -p %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}.d/

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/var/lib/consul

# Remember some releases don't use _unitdir..
mkdir -p %{buildroot}/usr/lib/systemd/system
cp -p %{SOURCE2} %{buildroot}/usr/lib/systemd/system/

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}.d/%{name}-server.json.sample
%config(noreplace) %{_sysconfdir}/%{name}.d/%{name}-agent.json
%attr(0750,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
/usr/lib/systemd/system/%{name}.service
%dir %attr(0750, consul, consul) /var/lib/consul

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
