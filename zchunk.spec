#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library for generating easy-to-delta files
Summary(pl.UTF-8):	Biblioteka do generowania plików pozwalających na łatwe generowanie różnic
Name:		zchunk
Version:	1.1.8
Release:	1
License:	BSD
Group:		Applications/File
#Source0Download: https://github.com/zchunk/zchunk/releases
Source0:	https://github.com/zchunk/zchunk/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4174e5533c4c1da1df36cf797191131a
URL:		https://github.com/zchunk/zchunk
BuildRequires:	curl-devel
BuildRequires:	gcc >= 5:3.2
BuildRequires:	meson >= 0.44.0
BuildRequires:	ninja >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	zstd-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
zchunk is a compressed file format that splits the file into
independent chunks. This allows you to only download changed chunks
when downloading a new version of the file, and also makes zchunk
files efficient over rsync.

zchunk files are protected with strong checksums to verify that the
file you downloaded is, in fact, the file you wanted.

%description -l pl.UTF-8
zchunk to format skompresowanych plików dzielący plik na niezależne
części. Pozwala to pobierać tylko zmienione części przy ściąganiu
nowej wersji pliku oraz czyni format wydajnym dla rsynca.

Plik zchunk są chronione silnymi sumami kontrolnymi w celu
weryfikacji, czy pobrany plik jest faktycznie tym, którym miał być.

%package libs
Summary:	Shared zck library
Summary(pl.UTF-8):	Biblioteka współdzielona zck
Group:		Libraries

%description libs
zchunk is a compressed file format that splits the file into
independent chunks. This allows you to only download changed chunks
when downloading a new version of the file, and also makes zchunk
files efficient over rsync.

zchunk files are protected with strong checksums to verify that the
file you downloaded is, in fact, the file you wanted.

This package contains shared library.

%description libs -l pl.UTF-8
zchunk to format skompresowanych plików dzielący plik na niezależne
części. Pozwala to pobierać tylko zmienione części przy ściąganiu
nowej wersji pliku oraz czyni format wydajnym dla rsynca.

Plik zchunk są chronione silnymi sumami kontrolnymi w celu
weryfikacji, czy pobrany plik jest faktycznie tym, którym miał być.

Ten pakiet zawiera bibliotekę współdzieloną.

%package devel
Summary:	Header files for zck library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki zck
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssl-devel
Requires:	zstd-devel

%description devel
Header files for zck library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki zck.

%package static
Summary:	Static zck library
Summary(pl.UTF-8):	Statyczna biblioteka zck
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static zck library.

%description static -l pl.UTF-8
Statyczna biblioteka zck.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/unzck
%attr(755,root,root) %{_bindir}/zck
%attr(755,root,root) %{_bindir}/zck_delta_size
%attr(755,root,root) %{_bindir}/zck_gen_zdict
%attr(755,root,root) %{_bindir}/zck_read_header
# R: curl
%attr(755,root,root) %{_bindir}/zckdl
%{_mandir}/man1/unzck.1*
%{_mandir}/man1/zck.1*
%{_mandir}/man1/zck_delta_size.1*
%{_mandir}/man1/zck_gen_zdict.1*
%{_mandir}/man1/zck_read_header.1*
%{_mandir}/man1/zckdl.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzck.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzck.so.1

%files devel
%defattr(644,root,root,755)
%doc zchunk_format.txt
%attr(755,root,root) %{_libdir}/libzck.so
%{_includedir}/zck.h
%{_pkgconfigdir}/zck.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzck.a
%endif
