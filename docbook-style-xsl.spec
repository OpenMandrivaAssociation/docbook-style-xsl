%define sgmlbase %{_datadir}/sgml/

Summary:	Norman Walsh's modular stylesheets for DocBook
Name:		docbook-style-xsl
Epoch:		1
Version:	1.79.2
Release:	10
Group:		Publishing
License:	Artistic style
Url:		http://sourceforge.net/projects/docbook
Source0:	https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F{%version}/docbook-xsl-nons-%{version}.tar.bz2
Source1:	%{name}.Makefile
Source2:	https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F{%version}/docbook-xsl-doc-%{version}.tar.bz2
#Avoid proportional-column-width for passivetex (bug #176766).
Patch1:		docbook-xsl-pagesetup.patch
#Hard-code the margin-left work around to expect passivetex (bug #113456).
Patch2:		docbook-xsl-marginleft.patch
#fix of #161619 - adjustColumnWidths now available
Patch3:		docbook-xsl-newmethods.patch
#change a few non-constant expressions to constant - needed for passivetex(#366441)
Patch4:		docbook-xsl-non-constant-expressions.patch
#added fixes for passivetex extension and list-item-body(#161371)
Patch5:		docbook-xsl-list-item-body.patch
#workaround missing mandir section problem (#727251)
Patch6:		docbook-xsl-mandir.patch
#Non-recursive string.subst that doesn't kill smb.conf.5 generation
Patch7:		docbook-style-xsl-non-recursive-string-subst.patch
BuildArch:	noarch
Provides:	docbook-xsl = %{version}
Requires:	docbook-dtd-xml
Requires(post,postun):	sgml-common

%description
These XSL stylesheets allow to convert any DocBook document to another
printed (for example, RTF or PostScript) or online (for example, HTML) format.
They are highly customizable.

%package doc
Summary:	Documentation for DocBook stylesheets
Group:		Books/Computer books

%description doc
This package contains the documentation for these stylesheets:
structure, customization, etc.

%prep
%setup -c -T -n docbook-xsl-%{version}
tar jxf %{SOURCE0}
mv docbook-xsl-nons-%{version}/* .
pushd ..
tar jxf %{SOURCE2}
popd

cp -p %{SOURCE1} Makefile

%autopatch -p1

# fix of non UTF-8 files rpmlint warnings
for fhtml in $(find ./doc -name '*.html' -type f)
do
  iconv -f ISO-8859-1 -t UTF-8 "$fhtml" -o "$fhtml".tmp
  mv -f "$fhtml".tmp "$fhtml"
  sed -i 's/charset=ISO-8859-1/charset=UTF-8/' "$fhtml"
done

for f in $(find -name "*'*")
do
  mv -v "$f" $(echo "$f" | tr -d "'")
done

%build
# index jar files to please rpmlint
# jar -i extensions/*.jar

%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install BINDIR=$DESTDIR%{_bindir} DESTDIR=$DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}
cp -a VERSION.xsl $DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}/VERSION.xsl
ln -s xsl-stylesheets-%{version} \
        $DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets

# Don't ship the extensions (bug #177256).
rm -rf $DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets/extensions/*

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
%doc BUGS
%doc README
%doc TODO
%{sgmlbase}/docbook/xsl-stylesheets-%{version}
%{sgmlbase}/docbook/xsl-stylesheets

%files doc
%doc doc docsrc
