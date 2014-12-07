%define sgmlbase %{_datadir}/sgml/

Summary:	Norman Walsh's modular stylesheets for DocBook
Name:		docbook-style-xsl
Epoch:          1
Version:	1.76.1
Release:	4
Group:		Publishing
License:	Artistic style
Url:		http://sourceforge.net/projects/docbook
Source0:	http://prdownloads.sourceforge.net/docbook/docbook-xsl-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/docbook/docbook-xsl-doc-%{version}.tar.bz2
BuildArch:	noarch
Provides:	docbook-xsl = %{version}
Requires:	docbook-dtd-xml
Requires(pre):	sgml-common

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
mkdir -p %{buildroot}%{sgmlbase}/docbook/xsl-stylesheets-%{version} 
# Camille 2006-05-29: those are dummy files to be removed in future releases; 2006-01-23: removed
# rm -f doc/*/param.html doc/pi/pi.html
cp -a VERSION common eclipse extensions fo highlighting html htmlhelp images javahelp lib template xhtml xhtml-1_1 manpages profiling params slides tools website roundtrip %{buildroot}%{sgmlbase}/docbook/xsl-stylesheets-%{version}  

ln -sf xsl-stylesheets-%{version} \
	%{buildroot}%{sgmlbase}/docbook/xsl-stylesheets

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
%doc BUGS TODO README VERSION NEWS* COPYING INSTALL
%{sgmlbase}/docbook/xsl-stylesheets-%{version}
%{sgmlbase}/docbook/xsl-stylesheets

%files doc
%doc doc docsrc

