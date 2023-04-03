# https://fedoraproject.org/wiki/How_to_create_an_RPM_package
# Built on Fedora and maintained by John Boero - jboero@hashicorp.com
# In honor of Seth Vidal https://www.redhat.com/it/blog/thank-you-seth-vidal

Name:           boundary-ui
Version:        1.5.1
Release:        1%{?dist}
Summary:        HashiCorp Boundary UI for Linux
License:        MPL
# Our engineering uses "amd64" instead of "x86_64" so ugly mapping...
Source0:        https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz
Source1:        https://github.com/jboero/hashicorpcopr/raw/master/boundary_icon.svg

BuildRequires:  coreutils git (yarn or yarnpkg) (npm < 17) xz-lzma-compat nodejs dpkg fakeroot
Requires(post): coreutils boundary nodejs
URL:            https://www.boundaryproject.io/

%define debug_package %{nil}

%description
Desktop client for Boundary UI simplifies operations of HashiCorp Boundary.

%prep
tar -xzf %{SOURCE0}

%build
ls
cd %{name}-%{version}
yarn install
yarn build:ui:desktop
yarn build:ui:desktop:app
#upx ui/desktop/electron-app/out/Boundary-linux-*/Boundary

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_datadir}
cd %{name}-%{version}
mv ui/desktop/electron-app/out/Boundary-linux-* %{buildroot}%{_datadir}/%{name}

# Symlink to system boundary depedency instead of duplicating it.
ln -sf /usr/bin/boundary %{buildroot}%{_datadir}/%{name}/resources/app/cli/boundary

# If anybody finds out how to write heredocs in rpm spec, let me know....
%{__cat} <<EOF  > %{buildroot}%{_bindir}/%{name}
#!/bin/bash
cd %{_datadir}/%{name}
%{_datadir}/%{name}/boundary-desktop --no-sandbox
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

mkdir -p %{buildroot}%{_datadir}/applications
%{__cat} <<EOF  > %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Comment[en_US]=
Comment=
Exec=/usr/bin/boundary-ui --no-sandbox
GenericName[en_US]=HashiCorp Boundary UI Client
GenericName=HashiCorp Boundary UI Client
Icon=%{_datadir}/icons/hicolor/scalable/apps/boundary_icon.svg
MimeType=
Name[en_US]=Boundary UI
Name=Boundary UI
Path=/usr/share/boundary-ui
StartupNotify=true
Terminal=false
TerminalOptions=
Type=Application
X-DBUS-ServiceName=
X-DBUS-StartupType=
X-KDE-SubstituteUID=false
X-KDE-Username=
EOF

%clean
rm -rf %{buildroot}
#rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/boundary_icon.svg

%pre

%post

%postun

%changelog
