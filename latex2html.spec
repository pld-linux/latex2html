Summary:	LaTeX to html translator
Summary(pl):	Konwerter z LaTeX-a do HTML
Name:		latex2html
Version:	99.2beta8
Release:	1
License:	GPL
Group:		Applications/Publishing/TeX
Group(de):	Applikationen/Publizieren/TeX
Group(es):	Aplicaciones/Editoración/TeX
Group(pl):	Aplikacje/Publikowanie/TeX
Group(pt_BR):	Aplicações/Editoração/TeX
Source0:	http://www.ctan.org/tex-archive/support/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-perl.patch
Patch1:		%{name}-tmp.patch
URL:		http://www.xray.mpe.mpg.de/mailing-lists/latex2html/
BuildRequires:	perl
BuildRequires:	tetex-latex
BuildRequires:	tetex-dvips
BuildRequires:	ghostscript
BuildRequires:	tetex-latex
BuildRequires:	tetex-dvips
BuildRequires:	netpbm-devel
BuildRequires:	netpbm-progs
BuildRequires:	giftrans
Requires:	perl >= 5.004
Requires:	ghostscript >= 4.03
Requires:	tetex-latex >= 0.4
Requires:	tetex-dvips >= 0.4
Requires:	ghostscript >= 4.03
Requires:	giftrans
Requires:	netpbm-progs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch

%define		_libdir		%{_datadir}/%{name}

%description
Elaborate perl program to convert latex documents to html, using LaTeX
to process images and equations.

%description -l pl
Program w perlu do konwertowania dokumentów LaTeXa do formatu HTML.
Generuje strony html oraz odpowiednie obrazki.

%prep 
%setup -q
%patch0 -p1
%patch1 -p1

%build
GS_LIB=.:%{_datadir}/ghostscript/lib:%{_datadir}/fonts/type1; export GS_LIB
%configure2_13 \
	--enable-images \
	--enable-pk \
	--enable-eps \
	--enable-gif \
	--enable-png \
	--enable-pipes \
	--enable-paths \
	--enable-wrapper \
	--with-perl=%{_bindir}/perl \
	--with-gs=%{_bindir}/gs \
	--with-rgb=%{_prefix}/X11R6/lib/X11/rgb.txt \
	--with-texpath=%{_datadir}/texmf/tex/latex/%{name} \
	--with-iconpath=/icons/l2h/

%{__make}

# build foilhtml modules
cd foilhtml && latex foilhtml.ins && cd ..

# build documentation
TEXINPUTS="../:../texinputs:$TEXINPUTS"; export TEXINPUTS
# FIXME
# make -C docs manual.dvi manual.html L2H="../latex2html"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/home/httpd/icons

cp -f cfgcache.pm cfgcache.pm.orig
cat << EOF >> cfgcache.pm

\$cfg{'BINDIR'} = q'$RPM_BUILD_ROOT%{_bindir}';
\$cfg{'LIBDIR'} = q'$RPM_BUILD_ROOT%{_libdir}';
\$cfg{'TEXPATH'} = q'$RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/latex2html';      

EOF

%{__make} install 
install  cfgcache.pm.orig $RPM_BUILD_ROOT%{_libdir}/cfgcache.pm
ln -sf	%{_libdir}/cweb2html/cweb2html $RPM_BUILD_ROOT%{_bindir}/cweb2html
ln -sf	%{_libdir}/icons $RPM_BUILD_ROOT/home/httpd/icons/l2h

rm -rf	$RPM_BUILD_ROOT%{_libdir}/{docs,example,foilhtml/foilhtml.log}

gzip -9nf BUGS FAQ LICENSE README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x %{_bindir}/texhash ]; then
	%{_bindir}/texhash
fi
if [ -x %{_bindir}/mktexlsr ]; then
	%{_bindir}/mktexlsr
fi

%files
%defattr(644,root,root,755)
%doc *gz
# FIXME
# %doc docs/manual/*.{gif,html,css}
%attr(-,  root,root) %{_libdir}
%attr(755,root,root) /home/httpd/icons/l2h
%attr(755,root,root) %{_bindir}/*
