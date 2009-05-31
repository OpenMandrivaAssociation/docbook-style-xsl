%define Name docbook-style-xsl
%define version 1.75.1
%define Release %mkrel 1

Name:		%{Name}
Version:	%{version}
Release:	1
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

%Description
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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{sgmlbase}/docbook/xsl-stylesheets-%{version} 
# Camille 2006-05-29: those are dummy files to be removed in future releases; 2006-01-23: removed
# rm -f doc/*/param.html doc/pi/pi.html
cp -a VERSION common eclipse extensions fo highlighting html htmlhelp images javahelp lib template xhtml manpages profiling params slides tools website roundtrip $RPM_BUILD_ROOT%{sgmlbase}/docbook/xsl-stylesheets-%{version}  

ln -sf xsl-stylesheets-%{version} \
	$RPM_BUILD_ROOT%{sgmlbase}/docbook/xsl-stylesheets

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc BUGS TODO README VERSION NEWS* COPYING RELEASE* INSTALL
%{sgmlbase}/docbook/xsl-stylesheets-%{version}
%{sgmlbase}/docbook/xsl-stylesheets

%files doc
%defattr (-,root,root)
%doc doc docsrc
