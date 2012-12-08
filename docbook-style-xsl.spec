Name:		docbook-style-xsl
Version:	1.76.1
Release:	%mkrel 1
Group:		Publishing
Summary:	Norman Walsh's modular stylesheets for DocBook
License:	Artistic style
URL:		http://sourceforge.net/projects/docbook
Provides:	docbook-xsl = %{version}
Requires:	docbook-dtd-xml
Requires(pre):	sgml-common >= 0.6.3-2mdk
# BuildRequires:	gcj-tools
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot 
Source0:	http://prdownloads.sourceforge.net/docbook/docbook-xsl-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/docbook/docbook-xsl-doc-%{version}.tar.bz2
BuildArch:	noarch

%define sgmlbase %{_datadir}/sgml/

%description
These XSL stylesheets allow to convert any DocBook document to another
printed (for example, RTF or PostScript) or online (for example, HTML) format.
They are highly customizable.

%package doc
Summary         : Documentation for DocBook stylesheets
Group       	: Books/Computer books

%description doc
This package contains the documentation for these stylesheets:
structure, customization, etc.
 

%prep
%setup -n docbook-xsl-%{version} -q
%setup -D -n docbook-xsl-%{version} -q -T -b 1

%build
# index jar files to please rpmlint
# jar -i extensions/*.jar

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{sgmlbase}/docbook/xsl-stylesheets-%{version} 
# Camille 2006-05-29: those are dummy files to be removed in future releases; 2006-01-23: removed
# rm -f doc/*/param.html doc/pi/pi.html
cp -a VERSION common eclipse extensions fo highlighting html htmlhelp images javahelp lib template xhtml xhtml-1_1 manpages profiling params slides tools website roundtrip $RPM_BUILD_ROOT%{sgmlbase}/docbook/xsl-stylesheets-%{version}  

ln -sf xsl-stylesheets-%{version} \
	%{buildroot}%{sgmlbase}/docbook/xsl-stylesheets

%clean
rm -rf %{buildroot}

#fix old buggy postun
%triggerpostun -- docbook-style-xsl < 1.67.2-2mdk
CATALOG=/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://docbook.sourceforge.net/release/xsl/%{version}" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://docbook.sourceforge.net/release/xsl/%{version}" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://docbook.sourceforge.net/release/xsl/current" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://docbook.sourceforge.net/release/xsl/current" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG


%post
CATALOG=/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://docbook.sourceforge.net/release/xsl/%{version}" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://docbook.sourceforge.net/release/xsl/%{version}" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://docbook.sourceforge.net/release/xsl/current" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://docbook.sourceforge.net/release/xsl/current" \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG


%postun
# do not remove on upgrade
CATALOG=/etc/xml/catalog
if [ "$1" = "0" -a -x %{_bindir}/xmlcatalog -a -f $CATALOG ]; then
  %{_bindir}/xmlcatalog --noout --del \
	"file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
fi

%files
%defattr (-,root,root)
%doc BUGS TODO README VERSION NEWS* COPYING INSTALL
%{sgmlbase}/docbook/xsl-stylesheets-%{version}
%{sgmlbase}/docbook/xsl-stylesheets

%files doc
%defattr (-,root,root)
%doc doc docsrc


%changelog
* Thu Oct 06 2011 Andrey Bondrov <abondrov@mandriva.org> 1.76.1-1mdv2012.0
+ Revision: 703307
- New version: 1.76.1

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.75.2-5
+ Revision: 663842
- mass rebuild

* Mon Nov 15 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 1.75.2-4mdv2011.0
+ Revision: 597783
- package xhtml-1_1 too

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.75.2-3mdv2010.1
+ Revision: 520693
- rebuilt for 2010.1

* Tue Oct 06 2009 Thierry Vignaud <tv@mandriva.org> 1.75.2-2mdv2010.0
+ Revision: 454763
- do not package huge release notes

* Thu Jul 23 2009 Frederik Himpe <fhimpe@mandriva.org> 1.75.2-1mdv2010.0
+ Revision: 398996
- update to new version 1.75.2

* Sun May 31 2009 Frederik Himpe <fhimpe@mandriva.org> 1.75.1-1mdv2010.0
+ Revision: 381608
- Add %%mkrel and clean up SPEC file a bit
- update to new version 1.75.1

* Wed Mar 18 2009 Funda Wang <fwang@mandriva.org> 1.74.3-1mdv2009.1
+ Revision: 357093
- New version 1.74.3

* Thu Jan 08 2009 Emmanuel Andry <eandry@mandriva.org> 1.74.0-1mdv2009.1
+ Revision: 327251
- New version 1.74.0

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.73.2-4mdv2009.0
+ Revision: 220678
- rebuild

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.73.2-3mdv2008.1
+ Revision: 149206
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Sep 06 2007 Camille Bégnis <camille@mandriva.com> 1.73.2-2mdv2008.0
+ Revision: 80885
- remove manpage patch not needed since 1.73.1

* Fri Aug 31 2007 Funda Wang <fwang@mandriva.org> 1.73.2-1mdv2008.0
+ Revision: 76391
- New version 1.73.2

* Thu Aug 16 2007 Thierry Vignaud <tv@mandriva.org> 1.73.0-3mdv2008.0
+ Revision: 64209
- rebuild

* Fri Jul 27 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.73.0-2mdv2008.0
+ Revision: 56415
- Added patch manpages_charmap from
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=249294
  Fixes a problem I saw while building git with latest
  docbook-style-xsl.

* Mon Jul 23 2007 Funda Wang <fwang@mandriva.org> 1.73.0-1mdv2008.0
+ Revision: 54721
- New version


* Wed Jan 24 2007 Camille Bégnis <camille@mandriva.com> 1.72.0-1mdv2007.0
+ Revision: 112758
- Import docbook-style-xsl

* Wed Jan 24 2007 Camille Begnis <camille@mandriva.com> 1.72.0-1mdv2007.1
- 1.72.0
- docsrc is back

* Thu Oct 05 2006 Camille Begnis <camille@mandriva.com> 1.71.0-1mdv2007.0
- New version 1.71.0

* Tue May 30 2006 Camille Begnis <camille@mandriva.com> 1.70.1-1mdv2007.0
- 1.70.1

* Wed Aug 17 2005 Camille Begnis <camille@mandriva.com> 1.69.1-1mdk
- 1.69.1
- replaces prereq with Requires(pre)

* Tue Jul 19 2005 Camille Begnis <camille@mandrakesoft.com> 1.69.0-1mdk
- 1.69.0
- doc is now in a separate archive

* Thu Feb 24 2005 Camille Begnis <camille@mandrakesoft.com> 1.68.1-1mdk
- 1.68.1

* Thu Feb 24 2005 Camille B�gnis <camille@mandrakesoft.com> 1.67.2-3mdk
- Rebuild

* Mon Feb 07 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 1.67.2-2mdk 
- Fix catalog registration on upgrade/uninstall

* Thu Dec 02 2004 Camille Begnis <camille@mandrakesoft.com> 1.67.2-1mdk
- 1.67.2
- remove unneeded libxml2-utils prereq...

* Tue Nov 23 2004 Camille Begnis <camille@mandrakesoft.com> 1.67.0-2mdk
- fix license to please rpmlint
- added libxml2-utils prereq for xmlcatalog [Bug 12470]

* Fri Nov 19 2004 Camille Begnis <camille@mandrakesoft.com> 1.67.0-1mdk
- 1.67.0
- adjust installation accordingly

* Tue Sep 14 2004 <camille@mandrakesoft.com> 1.66.0-1mdk
- New release 1.66.0

* Wed Apr 28 2004 <camille@mandrakesoft.com> 1.65.1-1mdk
- New release 1.65.1

