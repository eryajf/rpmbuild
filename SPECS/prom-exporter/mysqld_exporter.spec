%define debug_package %{nil}
%define user prometheus
%define group prometheus

Name:           mysqld_exporter
Version:        0.13.0
Release:        1.eryajf%{?dist}
Summary:        Prometheus exporter for MySQL server metrics.
License:        ASL 2.0
Packager:       https://github.com/eryajf
URL:            https://github.com/prometheus/mysqld_exporter

# 通常,你应该在公司内部搭建一个内网file程序,然后将一些日常构建所需的包放置在里边
Source0:        http://pkg.eryajf.net/package/prometheus//%{name}-%{version}.linux-amd64.tar.gz

# 为了便于区分SOURCE中的目录,故此处将需要的文件单独声明出来
%define         SourceFile1     %{name}.default
%define         SourceFile2     %{name}.init
%define         SourceFile3     my.cnf


Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts


%description
Prometheus exporter for MySQL server metrics. Supported MySQL versions: 5.1 and up. 
NOTE: Not all collection methods are supported on MySQL < 5.6



%prep
%setup -q -n %{name}-%{version}.linux-amd64


%build
/bin/true


%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile3} %{buildroot}%{_sysconfdir}/%{name}/my.cnf
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile1} %{buildroot}%{_sysconfdir}/default/%{name}
%if 0%{?el5}
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile2} %{buildroot}%{_initrddir}/%{name}
%else 
    install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile2} %{buildroot}%{_initddir}/%{name}
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
%config(noreplace) %{_sysconfdir}/%{name}/my.cnf
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%if 0%{?el5}
%{_initrdddir}/%{name}
%else
    %{_initddir}/%{name}
%endif
