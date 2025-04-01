%define debug_package %{nil}

Name:           blackbox_exporter
Version:        0.19.0
Release:        1.eryajf%{?dist}
Summary:        Blackbox prober exporter
License:        ASL 2.0
Packager:       https://github.com/eryajf
URL:            https://github.com/prometheus/blackbox_exporter

# 通常,你应该在公司内部搭建一个内网file程序,然后将一些日常构建所需的包放置在里边
Source0:        http://pkg.eryajf.net/package/prometheus/%{name}-%{version}.linux-amd64.tar.gz

# 为了便于区分SOURCE中的目录,故此处将需要的文件单独声明出来
%define         SourceFile1     %{name}.service
%define         SourceFile2     %{name}.default
%define         SourceFile3     %{name}.yml


%{?systemd_requires}
Requires(pre): shadow-utils

%description

The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP and ICMP.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile3} %{buildroot}%{_sysconfdir}/%{name}/blackbox.yml
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%caps(cap_net_raw=ep) %{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/blackbox.yml
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
