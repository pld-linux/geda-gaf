# TODO:
# - merge all stuff from geda-*/geda-*.spec
#
Summary:	Design Automation toolkit for electronic design
Name:		geda-gaf
Version:	1.6.2
Release:	0.1
License:	GPL v2+
Group:		Applications/Engineering
URL:		http://gpleda.org
Source0:	http://geda.seul.org/release/v1.6/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	35ae86aebc174ec1fc03863fde4c843c
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Patch0:		%{name}-git.patch
Patch1:		%{name}-build.patch

BuildRequires:	desktop-file-utils
BuildRequires:	gawk
BuildRequires:	intltool
BuildRequires:	gd-devel
BuildRequires:	gettext-tools
BuildRequires:	libtool
BuildRequires:	libltdl-devel
BuildRequires:	shared-mime-info

Requires:	geda-docs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	geda-gattrib = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	geda-gnetlist = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	geda-gschem = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	geda-gsymcheck = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	geda-utils = %{?epoch:%{epoch}:}%{version}-%{release}


%description
The GPL Electronic Design Automation (gEDA) project has produced and
continues working on a full GPL'd suite and toolkit of Electronic
Design Automation tools. These tools are used for electrical circuit
design, schematic capture, simulation, prototyping, and production.

Currently, the gEDA project offers a mature suite of free software
applications for electronics design, including schematic capture,
attribute management, bill of materials (BOM) generation, netlisting
into over 20 netlist formats, analog and digital simulation, and
printed circuit board (PCB) layout.


%package      -n  libgeda
Summary:	Libraries for the gEDA project
Group:		Development/Libraries
BuildRequires:	gtk+2-devel
BuildRequires:	guile-devel
Requires(post):	/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description  -n  libgeda
This package contains libgeda, the library needed by gEDA
applications.


%package      -n  libgeda-devel
Summary:	Development files for the libgeda library
Group:		Development/Libraries
Requires:	gtk+2-devel
Requires:	guile-devel
Requires:	libgeda = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	pkgconfig

%description  -n  libgeda-devel
Development files for libgeda library


%package      -n  geda-symbols
Summary:	Electronic symbols for gEDA
Group:		Applications/Engineering
BuildRequires:	transfig

%description  -n  geda-symbols
This package contains a bunch of symbols of electronic devices used by
gschem, the gEDA project schematic editor.


%package      -n  geda-docs
Summary:	Documentation and Examples for gEDA
Group:		Applications/Engineering
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
BuildArch:	noarch
%endif
Requires:	geda-symbols
Provides:	geda-examples = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	geda-examples < 20090830-2

%description  -n  geda-docs
This package contains documentation and examples for the gEDA project.


%package      -n  geda-gattrib
Summary:	Attribute editor for gEDA
Group:		Applications/Engineering
Requires:	geda-symbols

%description  -n  geda-gattrib
Gattrib is gEDA's attribute editor. It reads a set of gschem .sch
files (schematic files), and creates a spreadsheet showing all
components in rows, with the associated component attributes listed in
the columns. It allows the user to add, modify, or delete component
attributes outside of gschem, and then save the .sch files back out.
When it is completed, it will allow the user to edit attributes
attached to components, nets, and pins. (Currently, only component
attribute editing is implemented; pin attributes are displayed only,
and net attributes are TBD.)


%package      -n  geda-gnetlist
Summary:	Netlister for the gEDA project
Group:		Applications/Engineering
BuildRequires:	libstroke-devel
Requires:	geda-symbols

%description  -n  geda-gnetlist
Gnetlist generates netlists from schematics drawn with gschem (the
gEDA schematic editor). Possible output formats are:
- native
- tango
- spice
- allegro
- PCB
- verilog and others.


%package      -n  geda-gschem
Summary:	Electronics schematics editor
Group:		Applications/Engineering
Requires(pre):	libgeda = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	geda-docs
Requires:	geda-symbols

%description  -n  geda-gschem
Gschem is an electronics schematic editor. It is part of the gEDA
project.


%package      -n  geda-gsymcheck
Summary:	Symbol checker for electronics schematics editor
Group:		Applications/Engineering
Requires:	geda-symbols

%description  -n  geda-gsymcheck
Gsymcheck is a utility to check symbols for gschem. It is part of the
gEDA project.


%package      -n  geda-utils
Summary:	Several utilities for the gEDA project
Group:		Applications/Engineering
Requires:	geda-symbols
%if 0%{?fedora} > 6
BuildRequires:	perl-libs
%endif


%description  -n  geda-utils
Several utilities for the gEDA project.


%prep
%setup -q
%patch0 -p1 -b .RHBZ604288
%patch1 -p1

# Implicit DSO linking
# undefined reference to symbol 'atan2@@GLIBC_2.0'
sed -i "s|(gschem_LINK) \$(gschem_OBJECTS)|(gschem_LINK) -lm \$(gschem_OBJECTS)|" gschem/src/Makefile.in

# rpmlint UTF-8
for f in symbols/{AUTHORS,ChangeLog-1.0} gschem/ChangeLog; do
   iconv -f ISO-8859-1 -t UTF-8 $f > $f.tmp && \
      ( touch -r $f $f.tmp ; %{__mv} -f $f.tmp $f ) || \
      %{__rm} -f $f.tmp
done

# Fixing rpaths
%if "%{_libdir}" != "%{_prefix}/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

%build
%configure \
	--disable-static
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} INSTALL="%{_bindir}/install -p" install DESTDIR=$RPM_BUILD_ROOT


desktop-file-install --vendor "" \
    --dir $RPM_BUILD_ROOT%{_desktopdir} \
    --delete-original                          \
    $RPM_BUILD_ROOT%{_desktopdir}/geda-gschem.desktop \
    $RPM_BUILD_ROOT%{_desktopdir}/geda-gattrib.desktop


%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_desktopdir}/mimeinfo.cache
%{__rm} -f $RPM_BUILD_ROOT%{_datadir}/mime/{XMLnamespaces,aliases,generic-icons,globs,globs2,icons,magic,mime.cache,subclasses,treemagic,types}


# locale's
# libgeda38 => 1.6.2
# libgeda40 => 1.7.1
for i in libgeda38 libgeda40 geda-gattrib geda-gschem ; do
    if [ -d $RPM_BUILD_ROOT%{_localedir}/ ]; then
        for lang_dir in $RPM_BUILD_ROOT%{_localedir}/* ; do
            lang=$(basename $lang_dir)
            if [ -e $RPM_BUILD_ROOT%{_localedir}/$lang/LC_MESSAGES/$i.mo ] ; then
                echo "%lang($lang) %{_localedir}/$lang/LC_MESSAGES/$i.mo" >> $i.lang
            fi
        done
    fi
done

install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/{examples,gnetlist,gsymcheck,utils}

# gschem
install -pm 644 gschem/examples/*.sch    $RPM_BUILD_ROOT%{_docdir}/%{name}/examples
install -pm 644 gschem/examples/README.* $RPM_BUILD_ROOT%{_docdir}/%{name}/examples

# gnetlist
%{__cp} -pr gnetlist/tests $RPM_BUILD_ROOT%{_docdir}/%{name}/gnetlist
%{__cp} -pr gnetlist/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}/gnetlist
%{__cp} -pr gnetlist/examples/* $RPM_BUILD_ROOT%{_docdir}/%{name}/examples
%{__rm} -f $RPM_BUILD_ROOT%{_docdir}/%{name}/gnetlist/gnetlist.{1,doc}

# gsymcheck
%{__cp} -pr gsymcheck/tests/ $RPM_BUILD_ROOT%{_docdir}/%{name}/gsymcheck

# utils
%{__cp} -pr utils/tests $RPM_BUILD_ROOT%{_docdir}/%{name}/utils
%{__cp} -pr utils/examples $RPM_BUILD_ROOT%{_docdir}/%{name}/utils

find $RPM_BUILD_ROOT%{_docdir} -name 'Makefile*' -exec rm -f '{}' \;
%{__rm} -f $RPM_BUILD_ROOT%{_datadir}/mime/version
%{__rm} -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%post -n geda-symbols
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun -n geda-symbols
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans -n geda-symbols
update-mime-database %{_datadir}/mime &> /dev/null || :


%post -n geda-gschem
%update_icon_cache_post hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun -n geda-gschem
if [ $1 -eq 0 ] ; then
    %update_icon_cache_post hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans -n geda-gschem
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%post -n geda-gattrib
%update_icon_cache_post hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun -n geda-gattrib
if [ $1 -eq 0 ] ; then
    %update_icon_cache_post hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n geda-gattrib
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post -n libgeda
/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun -n libgeda
/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans -n libgeda
update-mime-database %{_datadir}/mime &> /dev/null || :

# Package Self test
%check
make distcheck

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%doc ABOUT-NLS AUTHORS ChangeLog COPYING* README NEWS


%files -n libgeda -f libgeda38.lang
%defattr(644,root,root,755)
%doc libgeda/{HACKING,ChangeLog*,BUGS,TODO}
%dir %{_datadir}/gEDA/
%dir %{_datadir}/gEDA/scheme
%{_libdir}/libgeda.so.*
%{_datadir}/gEDA/prolog.ps
%{_datadir}/gEDA/scheme/geda.scm
%{_datadir}/gEDA/system-gafrc
%{_datadir}/mime/packages/libgeda.xml

%files -n libgeda-devel
%defattr(644,root,root,755)
%{_includedir}/libgeda/
%{_libdir}/libgeda.so
%{_pkgconfigdir}/libgeda.pc


%files -n geda-symbols
%defattr(644,root,root,755)
%doc symbols/{AUTHORS,ChangeLog*,README,TODO}
%{_datadir}/gEDA/sym/
%dir %{_datadir}/gEDA/gafrc.d/
%{_datadir}/gEDA/gafrc.d/geda-clib.scm
%{_datadir}/mime/application/x-geda-symbol.xml
%{_iconsdir}/hicolor/*/mimetypes/application-x-geda-symbol.*
%{_datadir}/mime/application/x-geda-gsch2pcb-project.xml
%{_iconsdir}/hicolor/*/mimetypes/application-x-geda-gsch2pcb-project.*


%files -n geda-docs
%defattr(644,root,root,755)
%dir %{_docdir}/%{name}/
%doc %{_docdir}/%{name}/man
%doc %{_docdir}/%{name}/wiki
%doc %{_docdir}/%{name}/examples
%doc %{_docdir}/%{name}/gedadocs.html
%doc %{_docdir}/%{name}/nc.pdf


%files -n geda-gattrib -f geda-gattrib.lang
%defattr(644,root,root,755)
%doc gattrib/design/{gEDA_Structures_updated.png,ProgramArchitecture.gnumeric}
%doc gattrib/{BUGS,ChangeLog*,NOTES,README,ToDos}
%attr(755,root,root) %{_bindir}/gattrib
%{_datadir}/gEDA/system-gattribrc
%{_datadir}/gEDA/gattrib-menus.xml
%{_desktopdir}/geda-gattrib.desktop
%{_iconsdir}/hicolor/*/apps/geda-gattrib.*


%files -n geda-gnetlist
%defattr(644,root,root,755)
%doc gnetlist/{BUGS,ChangeLog*,TODO}
%doc %{_docdir}/%{name}/gnetlist
%attr(755,root,root) %{_bindir}/gnetlist
%attr(755,root,root) %{_bindir}/mk_verilog_syms
%attr(755,root,root) %{_bindir}/sch2eaglepos.sh
%attr(755,root,root) %{_bindir}/sw2asc
%{_datadir}/gEDA/scheme/gnet*.scm
%{_datadir}/gEDA/system-gnetlistrc
%{_mandir}/man1/gnetlist.*


%files -n geda-gschem -f geda-gschem.lang
%defattr(644,root,root,755)
%doc gschem/{BUGS,ChangeLog*,TODO}
%attr(755,root,root) %{_bindir}/gschem
%attr(755,root,root) %{_bindir}/gschemdoc
%{_datadir}/gEDA/scheme/auto-place-attribs.scm
%{_datadir}/gEDA/scheme/default-attrib-positions.scm
%{_datadir}/gEDA/scheme/image.scm
%{_datadir}/gEDA/scheme/pcb.scm
%{_datadir}/gEDA/scheme/print.scm
%{_datadir}/gEDA/scheme/auto-uref.scm
%{_datadir}/gEDA/scheme/generate_netlist.scm
%{_datadir}/gEDA/scheme/gschem.scm
%{_datadir}/gEDA/scheme/list-keys.scm
%{_datadir}/gEDA/scheme/print-NB-attribs.scm
%{_datadir}/gEDA/bitmap/gschem-*
%{_datadir}/gEDA/system-gschemrc
%{_datadir}/gEDA/gschem-gtkrc
%{_datadir}/gEDA/gschem-colormap-darkbg
%{_datadir}/gEDA/gschem-colormap-lightbg
%{_datadir}/gEDA/print-colormap-darkbg
%{_datadir}/gEDA/print-colormap-lightbg
%{_datadir}/gEDA/scheme/color-map.scm
%{_datadir}/mime/application/x-geda-schematic.xml
%{_desktopdir}/geda-gschem.desktop
%{_mandir}/man1/gschem.*
%{_iconsdir}/hicolor/*/apps/geda-gschem.*
%{_iconsdir}/hicolor/*/mimetypes/application-x-geda-schematic.*


%files -n geda-gsymcheck
%defattr(644,root,root,755)
%doc gsymcheck/{BUGS,ChangeLog*,TODO}
%doc %{_docdir}/%{name}/gsymcheck
%attr(755,root,root) %{_bindir}/gsymcheck
%{_datadir}/gEDA/system-gsymcheckrc
%{_mandir}/man1/gsymcheck.*


%files -n geda-utils
%defattr(644,root,root,755)
%doc utils/{ChangeLog*,README,AUTHORS}
%doc %{_docdir}/%{name}/utils
%doc %{_docdir}/%{name}/readmes/
%attr(755,root,root) %{_bindir}/garchive
%attr(755,root,root) %{_bindir}/grenum
%attr(755,root,root) %{_bindir}/gmk_sym
%attr(755,root,root) %{_bindir}/smash_megafile
%attr(755,root,root) %{_bindir}/convert_sym
%attr(755,root,root) %{_bindir}/sarlacc_schem
%attr(755,root,root) %{_bindir}/sarlacc_sym
%attr(755,root,root) %{_bindir}/gschupdate
%attr(755,root,root) %{_bindir}/gsymfix.pl
%attr(755,root,root) %{_bindir}/pcb_backannotate
%attr(755,root,root) %{_bindir}/gschlas
%attr(755,root,root) %{_bindir}/olib
%attr(755,root,root) %{_bindir}/refdes_renum
%attr(755,root,root) %{_bindir}/gsch2pcb
%attr(755,root,root) %{_bindir}/pads_backannotate
%attr(755,root,root) %{_bindir}/tragesym
%attr(755,root,root) %{_bindir}/gsymupdate
%attr(755,root,root) %{_bindir}/gxyrs
%attr(755,root,root) %{_bindir}/gnet_hier_verilog.sh
%{_datadir}/gEDA/system-gschlasrc
%{_mandir}/man1/grenum.1*
%{_datadir}/gEDA/perl/lib/gxyrs.pm
