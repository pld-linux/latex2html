Summary:	latex to html translator
Summary:	konwerter z latex'a do html'a
Name:		latex2html
Version:	99.2alpha13
Release:	1
Group:		Applications/Publishing/TeX
Group(pl):	Aplikacje/Publikowanie/TeX
Source0:	http://saftsack.fs.uni-bayreuth.de/~latex2ht/%{name}-%{version}.tar.gz
Patch0:		latex2html-perl.patch
Patch1:         latex2html-tmp.patch
Copyright:	GPL
URL:		http://www.xray.mpe.mpg.de/mailing-lists/latex2html/
Requires:	perl >= 5.004
Requires:	ghostscript >= 4.03
Requires:       tetex-latex >= 0.4
Requires:       tetex-dvips >= 0.4
Requires:       ghostscript >= 4.03
Requires:       giftrans
Requires:       libgr-progs >= 2.0.13
BuildRoot:	/tmp/%{name}-%{version}-root
BuildArch:	noarch
BuildRequires:	perl
BuildRequires:	tetex-latex
BuildRequires:	tetex-dvips

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
%configure \
	--enable-wrapper \
	--enable-paths \
	--enable-pipes \
	--enable-png \
	--enable-gif \
	--enable-eps \
	--enable-images \
	--libdir=%{_datadir}/%{name} \
	--with-rgb=%{_prefix}/X11R6/lib/X11/rgb.txt \
	--with-texpath=%{_datadir}/texmf/tex/latex/%{name} \
	--with-iconpath=/icons/l2h/

make

# build foilhtml modules
cd foilhtml && latex foilhtml.ins && cd ..

# build documentation
TEXINPUTS="../:../texinputs:$TEXINPUTS"; export TEXINPUTS
# FIXME
# make -C docs manual.dvi manual.html L2H="../latex2html"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/home/httpd/icons

cp l2hcfg.pm l2hcfg.pm.orig
cat << EOF >> l2hcfg.pm

\$cfg{'BINDIR'} = q'$RPM_BUILD_ROOT%{_bindir}';
\$cfg{'LIBDIR'} = q'$RPM_BUILD_ROOT%{_datadir}/%{name}';

EOF

make install 
install -m644	l2hcfg.pm.orig		$RPM_BUILD_ROOT%{_datadir}/%{name}/l2hcfg.pm
ln -s		%{_datadir}/%{name}/cweb2html/cweb2html	$RPM_BUILD_ROOT%{_bindir}/cweb2html
ln -s		%{_datadir}/%{name}/icons		$RPM_BUILD_ROOT/home/httpd/icons/l2h
rm -rf		$RPM_BUILD_ROOT%{_datadir}/%{name}/{docs,example,foilhtml/foilhtml.log}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/bin/texhash ]; then
/usr/bin/texhash
fi

%files
%defattr(644,root,root,755)
%doc FAQ README README.dvips dot.latex2html-init
# FIXME
# %doc docs/manual/*.{gif,html,css}
%attr(-,  root,root) %{_datadir}/%{name}
%attr(755,root,root) /home/httpd/icons/l2h
%attr(755,root,root) %{_bindir}/*
