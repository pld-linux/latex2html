# say "gif" or "png" here
%define		graphic_format	gif
Summary:	latex to html translator
Summary:	konwerter z latex'a do html'a
Name:		latex2html
Version:	99.2alpha12
Release:	1
Group:		Applications/Publishing/TeX
Group(pl):	Aplikacje/Publikowanie/TeX
Source0:	http://saftsack.fs.uni-bayreuth.de/~latex2ht/%{name}-%{version}.tar.gz
Source1:	replace-cwd
Patch0:		latex2html-perl.patch
Patch1:		latex2html-paths.patch
Copyright:	unknown
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

%define l2hdir  %{_datadir}/texmf/tex/latex/%{name}

%prep 
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
install -m755 %{SOURCE1} .
LATEX2HTMLDIR="`pwd`"; export LATEX2HTMLDIR

# Configure for GIF and generate documentation
./install-test << EOF
y
y

%{graphic_format}




EOF

# build documentation
TEXINPUTS="..//:%{_datadir}/texmf/tex/{latex,latex209,generic}//:$TEXINPUTS"; export TEXINPUTS
make -C docs manual.dvi manual.html L2H="../latex2html"

# build foilhtml modules
cd foilhtml && latex foilhtml.ins && cd ..

# replace path
./replace-cwd %{_datadir}/%{name} \
  configure-pstoimg latex2html latex2html.config \
  local.pm ps2img-n pstoimg pstoimg_nopipes texexpand \
  docs/manual/*

rm -f *.bak docs/manual/*.bak

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{l2hdir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -a   {styles,versions,icons.png,icons.gif}   $RPM_BUILD_ROOT%{_datadir}/%{name}
install local.pm				$RPM_BUILD_ROOT/etc/%{name}/l2hpstoimg.cfg
install foilhtml/*.perl                         $RPM_BUILD_ROOT%{_datadir}/%{name}/styles
install	{cweb2html,foilhtml}/*.perl		$RPM_BUILD_ROOT%{_datadir}/%{name}/styles
install	{IndicTeX-HTML,XyMTeX-HTML}/*.perl	$RPM_BUILD_ROOT%{_datadir}/%{name}/styles
install Override.pm                             $RPM_BUILD_ROOT%{_datadir}/%{name}
install foilhtml/*.cfg				$RPM_BUILD_ROOT/etc/%{name}
install %{name}.config				$RPM_BUILD_ROOT/etc/%{name}
install {texinputs,foilhtml}/*.sty              $RPM_BUILD_ROOT%{l2hdir}
install	{IndicTeX-HTML,cweb2html}/*.sty		$RPM_BUILD_ROOT%{l2hdir}
ln -s	/etc/%{name}/l2hpstoimg.cfg		$RPM_BUILD_ROOT%{_datadir}/%{name}/local.pm
ln -s   /etc/%{name}/foilhtml.cfg               $RPM_BUILD_ROOT%{_datadir}/%{name}/foilhtml.cfg
ln -s   /etc/%{name}/latex2html.config		$RPM_BUILD_ROOT%{_datadir}/%{name}/latex2html.config
install -m 755 configure-pstoimg makemap \
	pstoimg pstoimg_nopipes texexpand \
	ps2img-n makeseg/makeseg \
	cweb2html/cweb2html			$RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 755 latex2html			$RPM_BUILD_ROOT%{_bindir}

if [ "%{graphic_format}" == "gif" ]; then
 ln -sf icons.gif                       $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
else
 ln -sf icons.png                       $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
fi
	
%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/bin/texhash ]; then
/usr/bin/texhash
fi

%files
%defattr(644,root,root,755)
%doc FAQ README README.dvips docs/manual/*.{gif,html,css} dot.latex2html-init

%attr(755,root,root) %dir /etc/%{name}
%attr(755,root,root) %dir %{_datadir}/%{name}
%attr(755,root,root) %dir %{_datadir}/%{name}/icons.gif
%attr(755,root,root) %dir %{_datadir}/%{name}/icons.png
%attr(755,root,root) %dir %{_datadir}/%{name}/icons
%attr(755,root,root) %dir %{_datadir}/%{name}/styles
%attr(755,root,root) %dir %{_datadir}/%{name}/versions
%attr(755,root,root) %dir %{l2hdir}
%attr(644,root,root) /etc/%{name}/*
%attr(644,root,root) %{_datadir}/%{name}/icons.gif/*
%attr(644,root,root) %{_datadir}/%{name}/icons.png/*
%attr(644,root,root) %{_datadir}/%{name}/styles/*
%attr(644,root,root) %{_datadir}/%{name}/versions/*
%attr(644,root,root) %{_datadir}/%{name}/Override.pm
%attr(644,root,root) %{_datadir}/%{name}/latex2html.config
%attr(644,root,root) %{_datadir}/%{name}/local.pm
%attr(755,root,root) %{_datadir}/%{name}/configure-pstoimg
%attr(755,root,root) %{_datadir}/%{name}/makemap
%attr(755,root,root) %{_datadir}/%{name}/makeseg
%attr(755,root,root) %{_datadir}/%{name}/pstoimg
%attr(755,root,root) %{_datadir}/%{name}/pstoimg_nopipes
%attr(755,root,root) %{_datadir}/%{name}/texexpand
%attr(755,root,root) %{_bindir}/%{name}
%attr(644,root,root) %{l2hdir}/*
