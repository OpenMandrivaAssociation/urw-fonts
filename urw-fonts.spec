%define build_rebuild 0
%{?_with_rebuild: %global build_rebuild 1}
%define		urwmdkver 2.0-16.1mdk

Summary:	The 35 standard PostScript fonts
Name:		urw-fonts
Version:	2.0
Release:	%mkrel 22

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
BuildRequires:	XFree86
Requires(post):	fontconfig
Requires(postun):	fontconfig

%description 
Free, good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.  The
fonts.dir file font names match the original Adobe names of the fonts
(e.g., Times, Helvetica, etc.).

Install the urw-fonts package if you need free versions of standard
PostScript fonts.

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

%post
[ -x %{_bindir}/fc-cache ] && %{_bindir}/fc-cache 

%postun
if [ "$1" = "0" ]; then
	[ -x %{_bindir}/fc-cache ] && %{_bindir}/fc-cache 
fi

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
