%define		status		stable
%define		pearname	Autoload
%define		php_min_version 5.2.0
%include	/usr/lib/rpm/macros.php
Summary:	%{pearname} - A tool and library to generate autoload code
Name:		php-theseer-Autoload
Version:	1.14.2
Release:	1
License:	BSD License
Group:		Development/Languages/PHP
Source0:	http://pear.netpirates.net/get/%{pearname}-%{version}.tgz
# Source0-md5:	6b8e12de818cec14f6338be1a9bdc382
URL:		https://github.com/theseer/Autoload
BuildRequires:	php-channel(pear.netpirates.net)
BuildRequires:	php-pear-PEAR >= 1:1.8.0
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.610
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
%dir %{php_pear_dir}/TheSeer
%{php_pear_dir}/TheSeer/Autoload
