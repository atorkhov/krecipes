Name:           krecipes
Version:        0.8.1
Release:        2%{?dist}
Summary:        Krecipes: Your Way to Cook with Tux!

Group:          Applications/Productivity
License:        GPL
URL:            http://krecipes.sourceforge.net/
Source0:        http://download.sourceforge.net/krecipes/krecipes-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs-devel > 3.1, sqlite-devel
Requires:       kdebase >= 3.1, sqlite

patch0:		krecipes-gcc4.patch

%description
Application to manage recipes and shopping-lists

%prep
%setup -q
%patch0 -p1 -b .gcc4


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
%configure --disable-rpath
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
--dir $RPM_BUILD_ROOT%{_datadir}/applications \
--vendor=fedora \
--add-category=X-Fedora \
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


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc TODO AUTHORS README COPYING ChangeLog
%{_bindir}/krecipes
%{_datadir}/applications/fedora-krecipes.desktop
%{_datadir}/apps/krecipes
%{_datadir}/icons/hicolor/*/apps/*


%changelog
* Sat Jul 30 2005 <dennis@ausil.us> - 0.8.1-2%{?dist}
- Remove hard requirement for qt-MySQL and qt-Postgresql
- add exlicit QT lib and include dirs  for x86_64 build
- Fix summary to not read like a marketing ploy.
* Sun Jul 24 2005 <dennis@ausil.us> - 0.8.1-1%{?dist}
- Initial build
