Name:           krecipes
Version:        1.0
Release:        0.2.beta2%{?dist}
Summary:        Application to manage recipes and shopping-lists

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://krecipes.sourceforge.net/
Source0:        http://download.sourceforge.net/krecipes/krecipes-%{version}-beta2.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  kdelibs3-devel
BuildRequires:  sqlite-devel
BuildRequires:  mysql-devel
BuildRequires:  postgresql-devel

%description
Krecipes is a program that lets you to manage your recipes, create
shopping lists, choose a recipe based on available ingredients and plan
your menu/diet in advance.


%prep
%setup -q -n %{name}-%{version}-beta2

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

%configure \
  --disable-rpath \
  --with-mysql \
  --with-postgresql \
  --with-sqlite

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
--dir $RPM_BUILD_ROOT%{_datadir}/applications \
--vendor=fedora \
--add-category=Application \
--add-category=Utility \
--add-category=KDE \
--add-category=Qt \
--delete-original \
$RPM_BUILD_ROOT%{_datadir}/applnk/Utilities/krecipes.desktop

## File lists
# locale's
%find_lang %{name} || touch %{name}.lang
# HTML
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d $RPM_BUILD_ROOT$HTML_DIR ]; then
for lang_dir in $RPM_BUILD_ROOT$HTML_DIR/* ; do
   lang=$(basename $lang_dir)
   echo "%lang($lang) %doc $HTML_DIR/$lang/*" >> %{name}.lang
done
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_datadir}/icons/crystalsvg || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_datadir}/icons/crystalsvg || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc TODO AUTHORS README COPYING ChangeLog
%{_bindir}/krecipes
%{_datadir}/applications/fedora-krecipes.desktop
%{_datadir}/apps/krecipes
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/crystalsvg/*/mimetypes/krecipes_file.png
%{_datadir}/mimelnk/*/*.desktop

%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.2.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 17 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0-0.1.beta2
- Update to 1.0beta2 as it fixes a crash that prevents krecipes from starting
  with sqlite backend.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.1-11
- re-enable mysql/postgresql support
- re-enable mostly harmless X11 patch 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Mar 31 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.9.1-9
- gcc43 patch (#433986)
- BR: gettext
- --without-mysql --without-postgresql

* Thu Mar 13 2008 Dennis Gilmore <dennis@ausil.us> - 0.9.1-8
- fix BuildRequires

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-7
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Dennis Gilmore <dennis@ausil.us> - 0.9.1-6
- rebuild for F8
- clarify license GPLv2+

* Sat Sep 02 2006 Dennis Gilmore <dennis@ausil.us> - 0.9.1-5
- rebuild for fc6

* Sat Feb 18 2006 Dennis Gilmore <dennis@ausil.us> - 0.9.1-4
-rebuild for fc5 

* Wed Dec 21 2005 Dennis Gilmore <dennis@ausil.us> - 0.9.1-3
-Rebuild for gcc 4.1
* Mon Dec 05 2005 Dennis Gilmore <dennis@ausil.us> - 0.9.1-2
- retag because patch wasnt uploaded
* Sun Dec 04 2005 Dennis Gilmore <dennis@ausil.us> - 0.9.1-1
- update to 0.9.1  this fixes a bug in mysql database creation
* Sat Dec 03 2005 Dennis Gilmore <dennis@ausil.us> - 0.9-3
- fix BuildRequies for libacl and add patch for X check.
* Wed Nov 30 2005 Dennis Gilmore <dennis@ausil.us> - 0.9-2
- fix missing files
* Wed Nov 30 2005 Dennis Gilmore <dennis@ausil.us> - 0.9-1
- update to 0.9
* Sat Oct 20 2005 Dennis Gilmore <dennis@ausil.us> - 0.8.1-3%{?dist}
- add BuildRequires desktop-file-utils  http://fedoraproject.org/wiki/QAChecklist
- add %post and %postun scriptlets  to notify of new icons per
- http://standards.freedesktop.org/icon-theme-spec/icon-theme-spec-latest.html#implementation_notes
* Sat Jul 30 2005 <dennis@ausil.us> - 0.8.1-2%{?dist}
- Remove hard requirement for qt-MySQL and qt-Postgresql
- add exlicit QT lib and include dirs  for x86_64 build
- Fix summary to not read like a marketing ploy.

* Sun Jul 24 2005 <dennis@ausil.us> - 0.8.1-1%{?dist}
- Initial build
