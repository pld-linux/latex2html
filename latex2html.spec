#
#	Conditional build:
# _without_tex - don't build documentation using LaTeX
#
%include	/usr/lib/rpm/macros.perl
Summary:	LaTeX to html translator
Summary(pl):	Konwerter z LaTeX-a do HTML
Name:		latex2html
Version:	2002
%define	subv	1
Release:	2
License:	GPL
Group:		Applications/Publishing/TeX
Source0:	http://www.ctan.org/tex-archive/support/%{name}/%{name}-%{version}-%{subv}.tar.gz
Patch0:		%{name}-perl.patch
Patch1:		%{name}-tmp.patch
Patch2:		%{name}-gslib.patch
URL:		http://www.xray.mpe.mpg.de/mailing-lists/latex2html/
BuildRequires:	ghostscript
BuildRequires:	giftrans
BuildRequires:	netpbm-devel
BuildRequires:	netpbm-progs
BuildRequires:	perl >= 5.004
BuildRequires:	rpm-perlprov
%if %{!?_without_tex:1}0
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-makeindex
%endif
Requires:	ghostscript >= 4.03
Requires:	giftrans
Requires:	netpbm-progs
Requires:	perl >= 5.004
Requires:	tetex-dvips >= 0.4
Requires:	tetex-latex >= 0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch

%define		_libdir		%{_datadir}/%{name}
%define		_shlibdir	%{_datadir}/%{name}

%description
Elaborate perl program to convert latex documents to html, using LaTeX
to process images and equations.

%description -l pl
Program w perlu do konwertowania dokumentów LaTeXa do formatu HTML.
Generuje strony html oraz odpowiednie obrazki.

%prep
%setup -q -n %{name}-%{version}-%{subv}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
GS_LIB=.:/usr/share/ghostscript/lib:/usr/share/fonts/Type1; export GS_LIB
%configure2_13 \
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
	--with-rgb=/usr/X11R6/lib/X11/rgb.txt \
	--with-texpath=/usr/share/texmf/tex/latex/%{name} \
	--with-iconpath=/icons/l2h/

%{__make}

%if %{!?_without_tex:1}0
# build foilhtml modules
cd foilhtml
latex foilhtml.ins
cd ..

# build documentation
TEXINPUTS="../:../texinputs:$TEXINPUTS"; export TEXINPUTS
%{__make} -C docs manual.dvi
%{__make} -C docs manual.dvi
%{__make} -C docs manual.ps
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/home/services/httpd/icons

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf	%{_shlibdir}/cweb2html/cweb2html $RPM_BUILD_ROOT%{_bindir}/cweb2html
ln -sf	%{_shlibdir}/icons $RPM_BUILD_ROOT/home/services/httpd/icons/l2h

rm -rf	$RPM_BUILD_ROOT%{_shlibdir}/{docs,example,foilhtml/foilhtml.log}

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
%doc BUGS FAQ LICENSE README TODO %{!?_without_tex:docs/manual.ps}
%attr(755,root,root) %{_bindir}/*
%dir %{_shlibdir}
%{_shlibdir}/[!c]*
%{_shlibdir}/c[!w]*
%dir %{_shlibdir}/cweb2html
%{_shlibdir}/cweb2html/[!c]*
%{_shlibdir}/cweb2html/cweb.*
%attr(755,root,root) %{_shlibdir}/cweb2html/cweb2html
/home/services/httpd/icons/l2h
