# https://fedoraproject.org/wiki/How_to_create_an_RPM_package
# Built on Fedora and maintained by John Boero - jboero@hashicorp.com
# In honor of Seth Vidal https://www.redhat.com/it/blog/thank-you-seth-vidal

Name:           boundary-ui
Version:        1.2.1
Release:        1%{?dist}
Summary:        HashiCorp Boundary UI for Linux
License:        MPL
# Our engineering uses "amd64" instead of "x86_64" so ugly mapping...
Source0:        https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz

BuildRequires:  coreutils git yarnpkg npm upx xz-lzma-compat
BuildRequires:  nodejs <= 15
Requires(post): coreutils ffmpeg-libs vulkan-loader libglvnd-egl nodejs <= 1:15.0
URL:            https://www.boundaryproject.io/

%define debug_package %{nil}

%description
Desktop client for Boundary UI simplifies operations of HashiCorp Boundary.

%prep
tar -xvzf %{SOURCE0}

%build
#tree
cd %{name}-%{version}
#export PATH="$PATH:$HOME/node_modules/ember-cli/bin"
#echo $PATH
yarn install
yarn build:ui:desktop:app
upx ui/desktop/electron-app/out/Boundary-linux-*/Boundary

%install
mkdir -p %{buildroot}%{_bindir}/
cd %{name}-%{version}
cp ui/desktop/electron-app/out/Boundary-linux-*/Boundary %{buildroot}%{_bindir}/boundary-ui

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/Boundary

%pre

%post

%postun

%changelog
