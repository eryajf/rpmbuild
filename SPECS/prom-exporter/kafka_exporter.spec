%define debug_package %{nil}
%define user prometheus
%define group prometheus

Name:           kafka_exporter
Version:        1.4.2
Release:        1.eryajf%{?dist}
Summary:        Kafka exporter for Prometheus. For other metrics from Kafka, have a look at the JMX exporter.
License:        ASL 2.0
Packager:       https://github.com/eryajf
URL:            https://github.com/danielqsj/kafka_exporter

# 通常,你应该在公司内部搭建一个内网file程序,然后将一些日常构建所需的包放置在里边
Source0:        http://pkg.eryajf.net/package/prometheus//%{name}-%{version}.linux-amd64.tar.gz

# 为了便于区分SOURCE中的目录,故此处将需要的文件单独声明出来
%define         SourceFile1     %{name}.default
%define         SourceFile2     %{name}.init


%{?systemd_requires}
Requires(pre): shadow-utils
%if 0%{?el6} || 0%{?el5}
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%endif


%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels,
written in Go with pluggable metric collectors.



%prep
%setup -q -n %{name}-%{version}.linux-amd64


%build
/bin/true


%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile1} %{buildroot}%{_sysconfdir}/default/%{name}
%if 0%{?el5}
install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile2} %{buildroot}%{_initrddir}/%{name}
%else 
    #%if 0%{?el6} 
    install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile2} %{buildroot}%{_initddir}/%{name}
    #%else
    #install -D -m 644 %{_sourcedir}/prom-exporter/%{name}/%{SourceFile1} %{buildroot}%{_unitdir}/%{name}.service
    #%endif
%endif


%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0


%post
#%if 0%{?el6} || 0%{?el5}
chkconfig --add %{name}
chmod 755 %{_initrddir}/%{name}
#%else
#%systemd_post %{name}.service
#%endif


%preun
#%if 0%{?el6} || 0%{?el5}
if [ $1 -eq 0 ] ; then
    service %{name} stop > /dev/null 2>&1
    chkconfig --del %{name}
fi
#%else
#%systemd_preun %{name}.service
#%endif


%postun
#%if 0%{?el6} || 0%{?el5} 
if [ "$1" -ge "1" ] ; then
    service %{name} condrestart >/dev/null 2>&1 || :
fi
#%else
#%systemd_postun %{name}.service
#%endif


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%if 0%{?el5}
%{_initrdddir}/%{name}
%else
    #%if 0%{?el6} 
    %defattr(755, %{user}, %{group})
    %{_initddir}/%{name}
    #%else
    #%{_unitdir}/%{name}.service
    #%endif
%endif