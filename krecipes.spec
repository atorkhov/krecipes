Name:           krecipes
Version:        0.8.1
Release:        1%{?dist}
Summary:        Krecipes: Your Way to Cook with Tux!

Group:          Applications/Productivity
License:        GPL
URL:            http://krecipes.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/krecipes/krecipes-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs-devel > 3.1, sqlite-devel
Requires:       kdebase >= 3.1, qt-MySQL, qt-PostgreSQL, sqlite

patch0:		krecipes-gcc4.patch

%description
Krecipes is a program that lets you to manage your 
recipes, create shopping lists, choose a recipe based 
on available ingredients and plan your menu/diet in advance.
Supports MySQL, Postgres and sqlite backends.

%prep
%setup -q
%patch0 -p1 -b .gcc4


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
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
%doc
%{_bindir}/krecipes
%{_datadir}/applications/fedora-krecipes.desktop
%{_datadir}/apps/krecipes
%{_datadir}/icons/hicolor/*/apps/*


%changelog
* Sun Jul 24 2005 <dennis@ausil.us> - 0.8.1-1%{?dist}
- Initial build
