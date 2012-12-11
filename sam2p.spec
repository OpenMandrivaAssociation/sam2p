%define build_plf 0
%{?_with_plf: %global build_plf 1}

# enablelzw = 0 (don't build with LZW compression support)
# enablelzw = 1 (build with LZW compression support)
# Currently we use enablelzw = 0 due to Unisys LZW patents.
%define enablelzw       0

%if %build_plf
%define enablelzw       1
%endif

%define		sam2pver	0.49.1
%define		tif22pnmver	0.14

Summary:	Convert raster images to PostScript or PDF
Name:		sam2p
Version:	0.44.14
Release:	1
License:	GPL
Source0:	http://code.google.com/p/sam2p/downloads/list/sam2p-0.49.1.tar.gz
Source1:	http://code.google.com/p/sam2p/downloads/list/tif22pnm-0.14.tar.gz
URL:		http://code.google.com/p/sam2p/downloads/list
Group:		Graphics
BuildRequires:	libjpeg-progs
BuildRequires:	libtiff-devel
BuildRequires:	libpng-devel
Requires:	netpbm
Requires:	ghostscript
Requires:	jpeg-progs

%description
sam2p is a UNIX command line utility written in ANSI C++ that converts
many raster (bitmap) image formats into Adobe PostScript or PDF files
and several other formats. The images are not vectorized. sam2p gives
full control to the user to specify standards-compliance, compression,
and bit depths. In some cases sam2p can compress an image 100 times
smaller than the PostScript output of many other common image
converters. sam2p provides ZIP, RLE and LZW (de)compression filters
even on Level1 devices.

%prep
%setup -q -n %{name}-%{sam2pver} -a 1


%build
# don't use icecream
PATH=/bin:/usr/bin:/usr/X11R6/bin
export PATH
autoconf

pushd tif22pnm-%{tif22pnmver}
%configure2_5x \
	--with-libtiff-idir=%{_includedir} \
	--with-libpng-idir=%{_includedir} \
	--with-libtiff-ldir=%{_libdir} \
	--with-libpng-ldir=%{_libdir}

sed -i -e 's/lpng /lpng -lm/' cc_help.sh

make

cp tif22pnm png22pnm ../
cp -p README ../README.tif22pnm
popd

%configure \
%if %build_plf
	--enable-lzw \
	--enable-gif
%endif

make

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 sam2p tif22pnm png22pnm $RPM_BUILD_ROOT%{_bindir}

%files
%defattr(-,root,root)
%doc COPYING
%doc README README.tif22pnm examples contrib
%{_bindir}/*

