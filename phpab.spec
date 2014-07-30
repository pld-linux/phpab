#
# Conditional build:
%bcond_without	tests		# build without tests

%define		status		stable
%define		pearname	Autoload
%define		php_min_version 5.2.0
%include	/usr/lib/rpm/macros.php
Summary:	PHP AutoloadBuilder CLI tool
Name:		phpab
Version:	1.14.2
Release:	1
License:	BSD License
Group:		Development/Languages/PHP
Source0:	http://pear.netpirates.net/get/%{pearname}-%{version}.tgz
# Source0-md5:	6b8e12de818cec14f6338be1a9bdc382
URL:		http://www.phpab.net/
BuildRequires:	php-channel(pear.netpirates.net)
BuildRequires:	php-pear-PEAR >= 1:1.8.0
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.610
%if %{with tests}
BuildRequires:	php(dom)
BuildRequires:	php(tokenizer)
BuildRequires:	php-phpunit-PHPUnit
BuildRequires:	php-theseer-DirectoryScanner >= 1.3.0
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(spl)
Requires:	php(tokenizer)
Requires:	php-channel(pear.netpirates.net)
Requires:	php-ezc-ConsoleTools >= 1.6
Requires:	php-pear
Requires:	php-theseer-DirectoryScanner >= 1.3.0
Suggests:	php(openssl)
Suggests:	php(phar)
Obsoletes:	php-theseer-Autoload < 1.14.2-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# exclude optional php dependencies
%define		_noautophp	php-openssl

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp}

%description
A tool and library to generate autoload code.

In PEAR status of this package is: %{status}.

%prep
%pear_package_setup
mv docs/Autoload/* .

# fixes for tests
cd .%{php_pear_dir}/tests/%{pearname}
mv tests/init.php{,.orig}
cat <<EOF | tee tests/init.php
<?php
require 'TheSeer/DirectoryScanner/autoload.php';
require 'TheSeer/Autoload/autoload.php';
EOF

%build
%if %{with tests}
cd .%{php_pear_dir}
PEAR_DIR=$(pwd)
cd tests/%{pearname}

phpunit \
	--include-path=$PEAR_DIR \
	-d date.timezone=UTC
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_pear_dir}}
%pear_package_install
install -p ./%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE install.log
%{php_pear_dir}/.registry/.channel.*/*.reg
%attr(755,root,root) %{_bindir}/phpab
%{php_pear_dir}/TheSeer/Autoload
