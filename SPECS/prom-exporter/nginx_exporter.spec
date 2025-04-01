%define debug_package %{nil}
%define user prometheus
%define group prometheus
# 源文件名字
%define SourceName nginx-prometheus-exporter

Name:           nginx_exporter
Version:        0.9.0
Release:        1.eryajf%{?dist}
Summary:        Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.
License:        ASL 2.0
Packager:       https://github.com/eryajf
URL:            https://github.com/nginxinc/nginx-prometheus-exporter

# 通常,你应该在公司内部搭建一个内网file程序,然后将一些日常构建所需的包放置在里边
Source0:        http://pkg.eryajf.net/package/prometheus/%{SourceName}_%{version}_linux_amd64.tar.gz

# 为了便于区分SOURCE中的目录,故此处将需要的文件单独声明出来
%define         SourceFile1     %{name}.unit
%define         SourceFile2     %{name}.default
%define         SourceFile3     %{name}.init


Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts


%description
NGINX Prometheus exporter makes it possible to monitor NGINX or NGINX Plus using Prometheus.


# 一些exporter目录非标准化,可在这里通过一些手段将之标准化
%prep
%setup -c -q -n %{name}-%{version}.linux_amd64
mv %{SourceName} %{name}


%build
/bin/true


%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile2} %{buildroot}%{_sysconfdir}/default/%{name}
%if 0%{?el5}
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile3} %{buildroot}%{_initrddir}/%{name}
%else
    install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile3} %{buildroot}%{_initddir}/%{name}
%endif


%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0


%post
chkconfig --add %{name}
chmod 755 %{_initrddir}/%{name}


%preun
if [ $1 -eq 0 ] ; then
    service %{name} stop > /dev/null 2>&1
    chkconfig --del %{name}
fi


%postun
if [ "$1" -ge "1" ] ; then
    service %{name} condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%if 0%{?el5}
%{_initrdddir}/%{name}
%else
    %{_initddir}/%{name}
%endif