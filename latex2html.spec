# 
# TODO:
# - fix `--with tex' build
#
# Conditional build:
%bcond_with	tex	# try to build documentation using LaTeX
#
Summary:	LaTeX to HTML translator
Summary(pl.UTF-8):	Konwerter z LaTeXa do HTML
Name:		latex2html
Version:	2025
Release:	1
License:	GPL v2
Group:		Applications/Publishing/TeX
Source0:	https://github.com/latex2html/latex2html/archive/refs/tags/v%{version}.tar.gz
# Source0-md5:	8c0bf887a457a6b3c3d05abf400e638f
URL:		http://www.latex2html.org/
BuildRequires:	ghostscript
BuildRequires:	giftrans
BuildRequires:	netpbm-devel
BuildRequires:	netpbm-progs
BuildRequires:	%{__perl}
BuildRequires:	rpm-perlprov
%if %{with tex}
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-ams
BuildRequires:	texlive-latex
BuildRequires:	texlive-makeindex
%endif
Requires:	apache-icons
Requires:	ghostscript >= 4.03
Requires:	giftrans
Requires:	netpbm-progs
Requires:	%{__perl}
Requires:	texlive-dvips 
Requires:	texlive-latex
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_datadir}/%{name}
%define		_shlibdir	%{_datadir}/%{name}

%define		texmfdir	/usr/share/texmf

%description
Elaborate Perl program to convert latex documents to html, using LaTeX
to process images and equations.

%description -l pl.UTF-8
Program w Perlu do konwertowania dokumentów LaTeXa do formatu HTML.
Generuje strony html oraz odpowiednie obrazki.

%prep
%setup -q

%build
GS_LIB=.:/usr/share/ghostscript/lib:/usr/share/fonts/Type1; export GS_LIB
%configure \
	--shlibdir=%{_datadir}/%{name} \
	--enable-images \
	--enable-pk \
	--enable-eps \
	--enable-gif \
	--enable-png \
	--enable-pipes \
	--enable-paths \
	--enable-wrapper \
	--with-perl=%{__perl} \
	--with-gs=/usr/bin/gs \
	--with-rgb=%{_datadir}/X11/rgb.txt \
	--with-texpath=%{texmfdir}/tex/latex/%{name} \
	--with-iconpath=/icons/l2h

%{__make}

%if %{with tex}
	# build foilhtml modules
	cd foilhtml
	latex foilhtml.ins
	cd ..
	
	# build documentation
	TEXINPUTS="../:../texinputs:$TEXINPUTS"; export TEXINPUTS
	%{__make} -j1 -C docs manual.dvi
	%{__make} -j1 -C docs manual.dvi
	%{__make} -j1 -C docs manual.ps
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/apache-icons

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf	%{_shlibdir}/cweb2html/cweb2html $RPM_BUILD_ROOT%{_bindir}/cweb2html
ln -sf	%{_shlibdir}/icons $RPM_BUILD_ROOT%{_datadir}/apache-icons/l2h

%{__rm} -r $RPM_BUILD_ROOT%{_shlibdir}/{docs,example}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/bin/texhash ]; then
	/usr/bin/texhash
fi
if [ -x /usr/bin/mktexlsr ]; then
	/usr/bin/mktexlsr
fi

%files
%defattr(644,root,root,755)
%doc BUGS FAQ LICENSE README.md TODO %{?with_tex:docs/manual.ps}
%attr(755,root,root) %{_bindir}/cweb2html
%attr(755,root,root) %{_bindir}/latex2html
%attr(755,root,root) %{_bindir}/pstoimg
%attr(755,root,root) %{_bindir}/texexpand
%dir %{_shlibdir}
%{_shlibdir}/[!c]*
%{_shlibdir}/c[!w]*
%dir %{_shlibdir}/cweb2html
%{_shlibdir}/cweb2html/[!c]*
%{_shlibdir}/cweb2html/cweb.*
%attr(755,root,root) %{_shlibdir}/cweb2html/cweb2html
%{texmfdir}/tex/latex/%{name}
%{_datadir}/apache-icons/l2h
