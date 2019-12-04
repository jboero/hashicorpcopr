# https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Name:		vault
Version:	1.3.0
Release:	1
Summary:	Vault is a tool for securely accessing secrets
License:	MPL
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.hcl
Source2:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.service
Source3:    https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.conf
Requires(pre):	shadow-utils
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
URL:		https://www.vaultproject.io/

%define debug_package %{nil}

%description
Vault secures, stores, and tightly controls access to tokens, passwords,
certificates, API keys, and other secrets in modern computing. Vault handles
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
cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}
cp -p %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# Note _unitdir isn't present on all environments.
mkdir -p %{buildroot}/usr/lib/systemd/system/
cp -p %{SOURCE2} %{buildroot}/usr/lib/systemd/system/

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.hcl
%attr(0750,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
/usr/lib/systemd/system/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
    useradd -r -d %{_sharedstatedir}/%{name} -g %{name} \
    -s /sbin/nologin -c "Vault secret management tool" %{name}
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
