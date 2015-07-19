%define build_rebuild 0
%{?_with_rebuild: %global build_rebuild 1}
%define		urwmdkver 2.0-16.1mdk

Summary:	The 35 standard PostScript fonts
Name:		urw-fonts
Version:	2.0
Release:	37

Source0:	http://heanet.dl.sourceforge.net/sourceforge/gs-fonts/ghostscript-fonts-std-8.11.tar.bz2
# this overwrites several of the fonts and fonts.dir with new versions
Source1:	ftp://ftp.gnome.ru/fonts/urw/release/urw-fonts-1.0.7pre40.tar.bz2
Source4:	urw-fonts-%{urwmdkver}.tar.bz2
Source5:	http://peoples.mandriva.com/~ghibo/urw-fonts-1.0.7pre40-nimbusmonl-fixed.tar.bz2

# addition of *-iso10646-1 lines
Patch0:		urw-fonts-2.0-fontscale.patch
Patch1:		urw-fonts-monospaced.patch
Patch2:		urw-fonts-2.0-fontscale-adobe-before-urw.patch
Patch3:		urw-fonts-2.0-split-adobestd35fontdir.patch
Patch4:		urw-fonts-monospaced2.patch

License:	GPL, URW holds copyright
Group:		System/Fonts/Type1
URL:		ftp://ftp.cs.wisc.edu/ghost/gnu/fonts/
BuildRoot:	%_tmppath/%name-%version-%release-root
BuildArch:	noarch
%if %build_rebuild
BuildRequires:	fontforge >= 1.0-0.20040703.2mdk
%endif

%description 
Free, good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.  The
fonts.dir file font names match the original Adobe names of the fonts
(e.g., Times, Helvetica, etc.).

Install the urw-fonts package if you need free versions of standard
PostScript fonts.

The fonts provided are:
URW-Avantgarde
URW-Bookman
URW Chancery
URW-Century Schoolbook
URW-Courier
URW-Dingbats
URW-Gothic
URW-Helvetica
URW-New Century Schoolbook
URW-Nimbus Sans
URW-Nimbus Roman No9
URW-Nimbus Mono
URW-Palatino
URW Palladio
URW-Standard Symbols
URW-Symbol
URW-Times
URW-Zapf Chancery
URW-Zapf Dingbats

%prep
%setup -q -c -a1 -a4 -a5
%patch0 -p1 -b .fontscale
%patch1 -p1 -b .mono
%patch2 -p1 -b .urw
%patch3 -p1 -b .split
%patch4 -p1 -b .mono2

%build
%if %build_rebuild
# Resave PFB fonts, so /FontBBox will result as executable array
cat > copypfb.ff <<EOF
#!/usr/bin/fontforge
Open(\$1);
myfamilyname = \$familyname;
myweight = \$weight;
if (\$weight == "Demibold")
  myweight = "DemiBold";
  Print ("Fixing weight to DemiBold");
endif
if (\$familyname == "URW Chancery L ")
  myfamilyname = "URW Chancery L";
  Print ("Fixing URW Chancery L familyname");
endif
SetFontNames(\$fontname,myfamilyname,\$fullname,myweight,\$copyright,\$fontversion + "_%{version}-%{release}");
Generate(\$2,"",3);
Print ("Rebuilt: ", \$fontname);
Quit(0);
EOF
chmod +x copypfb.ff

mkdir -p fonts_fixed fixed
for i in fonts/*.pfb; do
	./copypfb.ff $i fonts_fixed/`basename $i`
done
for i in *.pfb; do
	./copypfb.ff $i fixed/`basename $i`
done



%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1 \
	$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/adobestd35

%if %build_rebuild
# install original URW fonts (from ghostscript set)
install -m 644	fonts_fixed/*.afm \
		fonts_fixed/*.pfm \
		fonts_fixed/*.pfb \
			$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/
# install new versions with cyrillic glyphs (and overwrite original
# ones if needed)
install -m 644	fixed/*.afm \
		fixed/*.pfm \
		fixed/*.pfb \
			$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/
# install fonts.scale/fonts.dir
install -m 644 fonts/fonts.scale \
			$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/
install -m 644 fonts/fonts.scale \
			$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/fonts.dir
install -m 644 fonts/fonts.scale.adobe \
	$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/adobestd35/fonts.scale
install -m 644 fonts/fonts.scale.adobe \
        $RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/adobestd35/fonts.dir
%else
install -m 644	urw-fonts-%{urwmdkver}/*.afm \
	urw-fonts-%{urwmdkver}/*.pfm \
	urw-fonts-%{urwmdkver}/*.pfb \
	urw-fonts-%{urwmdkver}/fonts.dir \
	urw-fonts-%{urwmdkver}/fonts.scale \
		$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/
install -m 644 urw-fonts-%{urwmdkver}/fonts.scale.adobe \
	$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/adobestd35/fonts.scale
install -m 644 urw-fonts-%{urwmdkver}/fonts.dir.adobe \
	$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/adobestd35/fonts.dir
## copy fixed fonts
#cp -fp	n022003l.{afm,pfm,pfb} \
#	n022004l.{afm,pfm,pfb} \
#	n022023l.{afm,pfm,pfb} \
#	n022024l.{afm,pfm,pfb} \
#	$RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/
%endif

cd $RPM_BUILD_ROOT%{_datadir}/fonts/default/Type1/adobestd35
for i in ../*.pfb ../*.afm ../*.pfm; do \
	ln -s $i
done

(cd $RPM_BUILD_ROOT/usr/share/fonts/default/Type1
# X.org's mkfontdir messes up encoding order, using alphabetical one,
# so for now comment the next line.
#    mkfontdir .
)

mkdir -p %{buildroot}%_sysconfdir/X11/fontpath.d/
ln -s ../../..%_datadir/fonts/default/Type1 \
    %{buildroot}%_sysconfdir/X11/fontpath.d/type1-urw-fonts:pri=50
ln -s ../../..%_datadir/fonts/default/Type1/adobestd35 \
    %{buildroot}%_sysconfdir/X11/fontpath.d/type1-urw-fonts-adobestd35:pri=50

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc README ChangeLog COPYING
%if !%build_rebuild
%doc urw-fonts-%{urwmdkver}/README.mdk
%endif
%dir %{_datadir}/fonts/default/
%dir %{_datadir}/fonts/default/Type1
%dir %{_datadir}/fonts/default/Type1/adobestd35
%{_datadir}/fonts/default/Type1/fonts.dir
%{_datadir}/fonts/default/Type1/fonts.scale
%{_datadir}/fonts/default/Type1/*.afm
%{_datadir}/fonts/default/Type1/*.pfb
%{_datadir}/fonts/default/Type1/*.pfm
%{_datadir}/fonts/default/Type1/adobestd35/*.afm
%{_datadir}/fonts/default/Type1/adobestd35/*.pfb
%{_datadir}/fonts/default/Type1/adobestd35/*.pfm
%{_datadir}/fonts/default/Type1/adobestd35/fonts.dir
%{_datadir}/fonts/default/Type1/adobestd35/fonts.scale
%{_sysconfdir}/X11/fontpath.d/type1-urw-fonts:pri=50
%{_sysconfdir}/X11/fontpath.d/type1-urw-fonts-adobestd35:pri=50


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0-28mdv2011.0
+ Revision: 670751
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0-27mdv2011.0
+ Revision: 608117
- rebuild

* Wed Jan 20 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 2.0-26mdv2010.1
+ Revision: 494169
- fc-cache is now called by an rpm filetrigger

* Fri Dec 18 2009 StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org> 2.0-25mdv2010.1
+ Revision: 479953
- Update description, fixes bug 23857

* Mon Sep 28 2009 Olivier Blin <oblin@mandriva.com> 2.0-25mdv2010.0
+ Revision: 450401
- add bootstrap flag for fontconfig (from Arnaud Patard)
- drop incorrect XFree86 buildrequire (from Arnaud Patard)

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.0-24mdv2010.0
+ Revision: 427484
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 2.0-23mdv2009.1
+ Revision: 351446
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 2.0-22mdv2009.0
+ Revision: 225909
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.0-21mdv2008.1
+ Revision: 171157
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix URL

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Sep 25 2007 Andreas Hasenack <andreas@mandriva.com> 2.0-20mdv2008.0
+ Revision: 92914
+ rebuild (emptylog)

* Mon Sep 24 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 2.0-19mdv2008.0
+ Revision: 92673
- revert previous change (r54804: use type1/ as the destination
  dir, not Type1/). Some applications (or libraries) have a hardcoded
  reference to Type1/ and can't find the fonts if they're not there
  (at least xpdf and Imagemagick are broken, see #34054).

* Mon Jul 23 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 2.0-18mdv2008.0
+ Revision: 54804
- use type1/ as the destination dir, not Type1/
  (minor font paths cleanup)

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 2.0-17mdv2008.0
+ Revision: 48750
- fontpath.d conversion (#31756)
- minor cleanups


* Thu Mar 16 2006 Giuseppe Ghibà <ghibo@mandriva.com> 2.0-16.1mdk
- Fixed z003034l.pfb, due to broken //UniqueID line.

* Sat Mar 11 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.0-16mdk
- Fake FontBBox to match the one in original ghostscript-fonts-std-8.11
  (fix bug #21017, #13080).

* Thu Feb 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.0-15.3mdk
- don't package any fontconfig cache
- fix fc-cache call

* Sun Oct 16 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0-15.2mdk
- Requires(post & postun)
- %%mkrel
- fix date in previous changelog

* Mon Jun 27 2005 Giuseppe Ghibò <ghibo@mandriva.com> 2.0-15.1mdk
- Copy forgotten Source5 archive (with fixed mono fonts) into install tree.

* Sat Feb 12 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-15mdk
- Use Filippov's version 1.0.7pre40.
- Fix bug #12493 (added Source5 with fixed fonts).
- Change '-URW-Courier' to spacing 'm' instead of 'p' in 
  adobestd35/fonts.dir|scale.
- Use monospacing in 'Nimbus Mono L' fonts in
  adobestd35/fonts.dir|scale.
- Removed fonts.alias for monospace.

* Sat Aug 07 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-14mdk
- Use Filippov's version 1.0.7pre35.

* Thu Aug 05 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-13mdk
- Added Patch4 to have Adobe names in a standalone fonts.dir
  to avoid confusion with OOo.
- Added links into %%{_datadir}/default/fonts/Type1/adobestd35.

* Sat Jul 31 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-12mdk
- Added Source1 (Filippov's URW fonts version 1.0.7pre33).
- Dropped Mashrab Kuratov Source3 (merged into Valek Filippov fonts).
- Dropped Source2 (bold nimbus, merged into Filippov fonts).
- Rebuilt Source4 and fixing weight of some font from Demibold to DemiBold
  (avoid problems with mkfontscale).
- Removing trailing space (Source4) from "URW Chancery L " FamilyName.
- Added Patch2 so to list Adobe 35 std font names before URW.

* Thu Jan 29 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-11mdk
- Added %%build_rebuild conditional building flag.
- Fixed fonts for bug http://bugs.mandrakelinux.com/query.php?bug=94.
- Dropped Source1: fonts from 
  ftp://ftp.gnome.ru/fonts/urw/release/urw-fonts-1.0.7pre22.tar.bz2
  and new ghostscript-fonts-std-8.11.tar.bz2 are identical, so take the gs one.
- Rebuilt Patch0.

* Mon Aug 25 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.0-10mdk
- Add Source3: improved versions of some fonts (added missing cyrillic
  glyphs) by Mashrab Kuvatov

