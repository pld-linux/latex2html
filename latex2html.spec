Summary:	latex to html translator
Summary:	konwerter z latex'a do html'a
Name:		latex2html
Version:	98.1p1
Release:	1
Group:		Applications/Publishing/TeX
Group(pl):	Aplikacje/Publikowanie/TeX
Source0:	http://www-dsed.llnl.gov/files/programs/unix/latex2html/source/%{name}-%{version}.tar.gz
Source1:	correct-paths.sh
Patch0:		latex2html.perl.diff
Patch1:		latex2html.paths.diff
Copyright:	unknown
URL:		http://www-dsed.llnl.gov/files/programs/unix/latex2html/
Requires:	perl >= 5.003
Requires:	ghostscript >= 4.03
BuildRoot:	/tmp/%{name}-%{version}-root
BuildArch:	noarch
BuildPrereq:	perl
BuildPrereq:	tetex-latex
BuildPrereq:	tetex-dvips

%description
latex to html translator

%description -l pl
konwerter z latex'a do html'a

%prep 
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
install %{SOURCE1} .
export LATEX2HTMLDIR=`pwd`
./install-test << EOF

y

g




EOF

for a in configure-pstoimg latex2html pstoimg texexpand; do
./correct-paths.sh $a
done

cd foilhtml; latex foilhtml.ins; cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/latex2html,usr/{{,s}bin,lib/texmf/texmf/tex/latex/latex2html}}
install -d $RPM_BUILD_ROOT/usr/share/latex2html
cp -a   {styles,versions,icons.png,icons.gif} $RPM_BUILD_ROOT/usr/share/latex2html/
install texinputs/*.sty   $RPM_BUILD_ROOT/usr/lib/texmf/texmf/tex/latex/latex2html
install foilhtml/*.sty    $RPM_BUILD_ROOT/usr/lib/texmf/texmf/tex/latex/latex2html
install foilhtml/*.cfg    $RPM_BUILD_ROOT/etc/latex2html
ln -s   /etc/latex2html/foilhtml.cfg $RPM_BUILD_ROOT/usr/lib/texmf/texmf/tex/latex/latex2html/foilhtml.cfg
install foilhtml/*.perl   $RPM_BUILD_ROOT/usr/share/latex2html/styles
install Override.pm       $RPM_BUILD_ROOT/usr/share/latex2html
install local.pm          $RPM_BUILD_ROOT/etc/latex2html/l2hpstoimg.cfg
ln -s   /etc/latex2html/l2hpstoimg.cfg $RPM_BUILD_ROOT/usr/share/latex2html/local.pm
install latex2html.config $RPM_BUILD_ROOT/etc/latex2html/
ln -s   /etc/latex2html/latex2html.config $RPM_BUILD_ROOT/usr/share/latex2html/latex2html.config
install configure-pstoimg $RPM_BUILD_ROOT/usr/share/latex2html
install latex2html	  $RPM_BUILD_ROOT/usr/bin
install install-test      $RPM_BUILD_ROOT/usr/sbin/configure-latex2html
install configure-pstoimg $RPM_BUILD_ROOT/usr/sbin
install configure-pstoimg $RPM_BUILD_ROOT/usr/share/latex2html
install makemap makeseg/makeseg pstoimg pstoimg_nopipes texexpand \
	$RPM_BUILD_ROOT/usr/share/latex2html
	
%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/bin/texhash ]; then
/usr/bin/texhash
fi

%files
%defattr(644,root,root,755)
%doc FAQ README README.dvips

%attr(755,root,root) %dir /etc/latex2html
%attr(755,root,root) %dir /usr/share/latex2html
%attr(755,root,root) %dir /usr/share/latex2html/icons.gif
%attr(755,root,root) %dir /usr/share/latex2html/icons.png
%attr(755,root,root) %dir /usr/share/latex2html/styles
%attr(755,root,root) %dir /usr/share/latex2html/versions
%attr(755,root,root) %dir /usr/lib/texmf/texmf/tex/latex/latex2html
%attr(644,root,root) /etc/latex2html/*
%attr(644,root,root) /usr/share/latex2html/icons.gif/*
%attr(644,root,root) /usr/share/latex2html/icons.png/*
%attr(644,root,root) /usr/share/latex2html/styles/*
%attr(644,root,root) /usr/share/latex2html/versions/*
%attr(644,root,root) /usr/share/latex2html/Override.pm
%attr(644,root,root) /usr/share/latex2html/latex2html.config
%attr(644,root,root) /usr/share/latex2html/local.pm
%attr(755,root,root) /usr/share/latex2html/configure-pstoimg
%attr(755,root,root) /usr/share/latex2html/makemap
%attr(755,root,root) /usr/share/latex2html/makeseg
%attr(755,root,root) /usr/share/latex2html/pstoimg
%attr(755,root,root) /usr/share/latex2html/pstoimg_nopipes
%attr(755,root,root) /usr/share/latex2html/texexpand
%attr(755,root,root) /usr/bin/latex2html
%attr(644,root,root) /usr/lib/texmf/texmf/tex/latex/latex2html/*

%changelog
* Thu Feb 10 1999 Arkadiusz Mi¶kieiwcz <misiek@pld.org.pl>
 - initial PLD release
