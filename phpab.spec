#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_min_version 5.3.0
Summary:	PHP AutoloadBuilder CLI tool
Name:		phpab
Version:	1.29.4
Release:	2
License:	BSD
Group:		Development/Languages/PHP
Source0:	https://github.com/theseer/Autoload/archive/%{version}/Autoload-%{version}.tar.gz
# Source0-md5:	a51a99c6e934074801afe51e5b8fda6e
URL:		https://github.com/theseer/Autoload
BuildRequires:	%{_bindir}/php
BuildRequires:	php(tokenizer)
BuildRequires:	rpmbuild(macros) >= 1.610
%if %{with tests}
BuildRequires:	php(dom)
BuildRequires:	php-phpunit-PHPUnit
BuildRequires:	php-theseer-DirectoryScanner >= 1.3.3
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(spl)
Requires:	php(tokenizer)
Requires:	php-ezc-ConsoleTools >= 1.7
Requires:	php-theseer-DirectoryScanner >= 1.3.3
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

%prep
%setup -q -n Autoload-%{version}

# Fix autoloader paths: upstream uses composer vendor/ layout,
# we use system-installed packages in %%{php_pear_dir}.
# From install dir (%%{php_pear_dir}/TheSeer/Autoload/), the relative paths are:
#   ezc/Base       -> ../../ezc/Base/
#   ezc/ConsoleTools -> ../../ezc/ConsoleTools/
#   DirectoryScanner -> ../DirectoryScanner/
%{__sed} -i -e "s|/../vendor/zetacomponents/base/src/|/../../ezc/Base/|g" \
	-e "s|/../vendor/zetacomponents/console-tools/src/|/../../ezc/ConsoleTools/|g" \
	-e "s|/../vendor/theseer/directoryscanner/src/|/../DirectoryScanner/|g" \
	src/autoload.php

# Fix the entry point to use system autoloader path
%{__sed} -i -e '1s|#!/usr/bin/env php|#!%{__php}|' \
	-e '/vendor\/autoload/,/break;/d' \
	-e "s|__DIR__ . '/../../src/autoload.php'|'%{php_pear_dir}/TheSeer/Autoload/autoload.php'|" \
	-e "s/%%development%%/%{version}/" \
	composer/bin/phpab

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_pear_dir}/TheSeer/Autoload}
cp -a src/* $RPM_BUILD_ROOT%{php_pear_dir}/TheSeer/Autoload
install -p composer/bin/phpab $RPM_BUILD_ROOT%{_bindir}/phpab

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE CHANGELOG.md
%attr(755,root,root) %{_bindir}/phpab
%dir %{php_pear_dir}/TheSeer
%{php_pear_dir}/TheSeer/Autoload
