Name:       tizenclaw-skill-plugin-sample
Summary:    TizenClaw Skill Plugin Sample
Version:    1.1.0
Release:    1
Group:      System/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: tizen-manifest.xml
Source1002: %{name}.manifest
BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
Sample skill plugin for TizenClaw providing device info tools.
Demonstrates Python, Node.js, and native C++ skill runtimes.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%cmake .
%__make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}/usr/apps/org.tizen.tizenclaw-skill-plugin-sample
mkdir -p %{buildroot}/usr/share/packages
cp tizen-manifest.xml %{buildroot}/usr/share/packages/org.tizen.tizenclaw-skill-plugin-sample.xml
cp tizen-manifest.xml %{buildroot}/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/tizen-manifest.xml

# Signing
%define tizen_sign_base %{_prefix}/apps/org.tizen.tizenclaw-skill-plugin-sample
%define tizen_sign 1
%define tizen_author_sign 1
%define tizen_dist_sign 1

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
/usr/share/packages/org.tizen.tizenclaw-skill-plugin-sample.xml
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/tizen-manifest.xml
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_info/manifest.json
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_info/skill.py
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_status/manifest.json
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_status/skill.py
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_time_node/manifest.json
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_time_node/skill.js
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_load_native/manifest.json
%attr(755,root,root) /usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_load_native/get_sample_load_native
