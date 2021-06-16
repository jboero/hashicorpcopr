# https://fedoraproject.org/wiki/How_to_create_an_RPM_package
# Built and maintained by John Boero - jboero@hashicorp.com
# In honor of Seth Vidal https://www.redhat.com/it/blog/thank-you-seth-vidal

%define hashiarch %(if [ "%{_arch}" == 'x86_64' ]; then echo 'amd64'; elif [ "%{_arch}" == 'aarch64' ]; then echo 'arm64'; elif [ "%_arch" == 'i386' ]; then echo '386'; else echo "%{_arch}"; fi)

Name:		tfc-agent
Version:	0.2.1
Release:	1%{?dist}
Summary:	Terraform Agent runs TFC Business Tier jobs locally.
License:	MPL
# Our engineering uses "amd64" instead of "x86_64" so ugly mapping...
Source0:    https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_%{hashiarch}.zip
Source1:	  https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.service
Source2:    https://raw.githubusercontent.com/jboero/hashicorpcopr/master/%{name}.conf

BuildRequires:  systemd coreutils unzip upx
Requires(pre):	shadow-utils
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
URL:		https://www.terraform.io/

%define debug_package %{nil}

%description

%prep
%autosetup -c %{name}-%{version}

%build

%install
mkdir -p %{buildroot}%{_bindir}/
cp -p %{name}* %{buildroot}%{_bindir}/

# Note _unitdir isn't present on all environments.
mkdir -p %{buildroot}/usr/lib/systemd/system/
cp -p %{SOURCE1} %{buildroot}/usr/lib/systemd/system/

mkdir -p %{buildroot}%{_sysconfdir}/%{name} %{buildroot}%{_sysconfdir}/sysconfig
cp -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/


%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-core
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}.conf
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
