%define debug_package %{nil}

Name:           rabbitmq_exporter
Version:        1.0.0
Release:        1.eryajf%{?dist}
Summary:        Prometheus exporter for RabbitMQ metrics
License:        MIT
Packager:       https://github.com/eryajf
URL:            https://github.com/kbudde/rabbitmq_exporter


# 通常,你应该在公司内部搭建一个内网file程序,然后将一些日常构建所需的包放置在里边
Source0:        http://pkg.eryajf.net/package/prometheus/%{name}-%{version}-RC8.linux-amd64.tar.gz

# 为了便于区分SOURCE中的目录,故此处将需要的文件单独声明出来
%define         SourceFile1     %{name}.service
%define         SourceFile2     %{name}.default


%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for RabbitMQ metrics.

%prep
%setup -q -n %{name}-%{version}-RC8.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
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
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus