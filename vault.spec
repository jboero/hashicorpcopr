# https://fedoraproject.org/wiki/How_to_create_an_RPM_package
# Built and maintained by John Boero - jboero@hashicorp.com
# In honor of Seth Vidal https://www.redhat.com/it/blog/thank-you-seth-vidal

%define hashiarch %(if [ "%{_arch}" == 'x86_64' ]; then echo 'amd64'; elif [ "%{_arch}" == 'aarch64' ]; then echo 'arm64'; elif [ "%_arch" == 'i386' ]; then echo '386'; else echo "%{_arch}"; fi)

Name:		vault
Version:	1.6.1
Release:	1%{?dist}
Summary:	Vault is a tool for securely accessing secrets
License:	MPL
# Our engineering uses "amd64" instead of "x86_64" so ugly mapping...
Source0:    https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_%{hashiarch}.zip
Source1:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.hcl
Source2:	https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.service
Source3:    https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.conf
Source4:    https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_arm.zip
Source5:    https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_386.zip
Source6:    https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.agent.hcl

BuildRequires:  systemd coreutils unzip upx
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
upx %{name}

%install

mkdir -p %{buildroot}%{_bindir}/
cp -p %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sysconfdir}/%{name} %{buildroot}%{_sysconfdir}/sysconfig
cp -p %{SOURCE1} %{SOURCE6} %{buildroot}%{_sysconfdir}/%{name}
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
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.agent.hcl
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}.conf
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
