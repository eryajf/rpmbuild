- 制作完成后的rpm包存放目录

## openresty

先下载依赖：

```sh
$ wget https://openresty.org/package/centos/openresty.repo
$ mv openresty.repo /etc/yum.repos.d/
$ yum check-update
$ for i in openresty-openssl111  openresty-pcre-8.45  openresty-zlib-1.2.13;do repotrack $i -p openresty;done
```

然后下载定制的包到openresty目录下。

```sh
$ cd openresty
$ wget https://github.com/eryajf/rpmbuild/raw/main/RPMS/x86_64/openresty-1.19.9.1-1.eryajf.el7.x86_64.rpm
```

执行安装命令：

```sh
$ yum localinstall -y *.rpm
```
