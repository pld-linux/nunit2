Summary:	Unit test framework for CLI
Summary(pl.UTF-8):	Szkielet testów jednostkowych dla CLI
Name:		nunit2
Version:	2.6.4
Release:	1
License:	BSD-like
Group:		Development/Tools
Source0:	https://github.com/nunit/nunitv2/archive/%{version}/nunitv2-%{version}.tar.gz
# Source0-md5:	d029438f8e497eabee41c2f8f282fe0b
Source1:	%{name}.pc
Source2:	%{name}-gui.sh
Source3:	%{name}-console.sh
Source4:	%{name}.desktop
URL:		http://www.nunit.org/
BuildRequires:	libgdiplus
BuildRequires:	mono-devel >= 4.0
BuildRequires:	rpmbuild(monoautodeps)
Requires:	dotnet-nunit2 = %{version}-%{release}
Obsoletes:	nunit-runner
ExclusiveArch:	%{ix86} %{x8664} arm aarch64 ia64 mips ppc ppc64 s390x sparc sparcv9 sparc64
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NUnit is a unit testing framework for all .NET languages. It serves
the same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

NUnit targets the CLI (Common Language Infrastructure) and supports
Mono and the Microsoft .NET Framework.

%description -l pl.UTF-8
NUnit to szkielet do testów jednostkowych dla wszystkich języków .NET.
Służy do tego samego celu, co JUnit w świecie Javy. Obsługuje
kategorie testów, testy pod kątem wyjątków oraz zapis wyników testów w
pliku tekstowym lub XML.

NUnit jest przeznaczony dla CLI (Common Language Infrastructure),
obsługuje Mono oraz Microsoft .NET Framework.

%package gui
Summary:	Tools for run NUnit test
Summary(pl.UTF-8):	Narzędzia do uruchamiania testów jednostkowych NUnit
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description gui
Desktop application for run NUnit test.

%description gui -l pl.UTF-8
Graficzna aplikacja do uruchamiania testów NUnit.

%package doc
Summary:	Documentation for NUnit 2.x
Summary(pl.UTF-8):	Dokumentacja do pakietu NUnit 2.x
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for NUnit 2.x.

%description doc -l pl.UTF-8
Dokumentacja do pakietu NUnit 2.x.

%package -n dotnet-nunit2
Summary:	NUnit 2.x library for .NET
Summary(pl.UTF-8):	Biblioteka NUnit 2.x dla .NET
Group:		Libraries
Requires:	mono >= 4.0

%description -n dotnet-nunit2
NUnit 2.x library for .NET.

%description -n dotnet-nunit2 -l pl.UTF-8
Biblioteka NUnit 2.x dla .NET.

%package -n dotnet-nunit2-devel
Summary:	Development files for NUnit 2.x
Summary(pl.UTF-8):	Pliki programistyczne pakietu NUnit 2.x
Group:		Development/Libraries
Requires:	dotnet-nunit2 = %{version}-%{release}
Requires:	mono-devel >= 4.0
Obsoletes:	nunit2-devel

%description -n dotnet-nunit2-devel
Development files for NUnit 2.x.

%description -n dotnet-nunit2-devel -l pl.UTF-8
Pliki programistyczne pakietu NUnit 2.x.

%prep
%setup -q -n nunitv2-%{version}

# force .NET 4 to avoid warnings with mono 4
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
xbuild /property:Configuration=Debug ./src/NUnitCore/core/nunit.core.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitCore/interfaces/nunit.core.interfaces.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitFramework/framework/nunit.framework.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitMocks/mocks/nunit.mocks.csproj
xbuild /property:Configuration=Debug ./src/ClientUtilities/util/nunit.util.dll.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console/nunit-console.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console-exe/nunit-console.exe.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui/nunit-gui.csproj
xbuild /property:Configuration=Debug ./src/GuiComponents/UiKit/nunit.uikit.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiException/UiException/nunit.uiexception.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui-exe/nunit-gui.exe.csproj

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_prefix}/lib/mono/nunit2,%{_pkgconfigdir},%{_desktopdir},%{_pixmapsdir}}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_pkgconfigdir}/nunit2.pc
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/nunit-gui26
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/nunit-console26
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/nunit2.desktop
cp src/GuiRunner/nunit-gui-exe/App.ico $RPM_BUILD_ROOT%{_pixmapsdir}/nunit2.ico
cp -p src/ConsoleRunner/nunit-console-exe/App.config $RPM_BUILD_ROOT%{_prefix}/lib/mono/nunit2/nunit-console.exe.config
cp -p src/GuiRunner/nunit-gui-exe/App.config $RPM_BUILD_ROOT%{_prefix}/lib/mono/nunit2/nunit.exe.config
find bin -name \*.dll -exec install "{}" "$RPM_BUILD_ROOT%{_prefix}/lib/mono/nunit2" \;
find bin -name \*.exe -exec install "{}" "$RPM_BUILD_ROOT%{_prefix}/lib/mono/nunit2" \;
for i in nunit-console-runner.dll nunit.core.dll nunit.core.interfaces.dll nunit.framework.dll nunit.mocks.dll nunit.util.dll ; do
	gacutil -i $RPM_BUILD_ROOT%{_prefix}/lib/mono/nunit2/$i -package nunit2 -root $RPM_BUILD_ROOT%{_prefix}/lib
done

%clean
rm -rf $RPM_BUILD_ROOT

%post gui
%update_desktop_database

%postun gui
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc README.md license.txt 
%attr(755,root,root) %{_bindir}/nunit-console26
%{_prefix}/lib/mono/nunit2/nunit-console.exe
%{_prefix}/lib/mono/nunit2/nunit-console.exe.config

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nunit-gui26
%{_prefix}/lib/mono/nunit2/nunit.exe
%{_prefix}/lib/mono/nunit2/nunit.exe.config
%{_prefix}/lib/mono/nunit2/nunit-gui-runner.dll
%{_desktopdir}/nunit2.desktop
%{_pixmapsdir}/nunit2.ico

%files doc
%defattr(644,root,root,755)
%doc doc/*

%files -n dotnet-nunit2
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gac/nunit-console-runner
%{_prefix}/lib/mono/gac/nunit.core
%{_prefix}/lib/mono/gac/nunit.core.interfaces
%{_prefix}/lib/mono/gac/nunit.framework
%{_prefix}/lib/mono/gac/nunit.mocks
%{_prefix}/lib/mono/gac/nunit.util
%dir %{_prefix}/lib/mono/nunit2
%{_prefix}/lib/mono/nunit2/nunit-console-runner.dll
%{_prefix}/lib/mono/nunit2/nunit.core.dll
%{_prefix}/lib/mono/nunit2/nunit.core.interfaces.dll
%{_prefix}/lib/mono/nunit2/nunit.framework.dll
%{_prefix}/lib/mono/nunit2/nunit.mocks.dll
%{_prefix}/lib/mono/nunit2/nunit.uiexception.dll
%{_prefix}/lib/mono/nunit2/nunit.uikit.dll
%{_prefix}/lib/mono/nunit2/nunit.util.dll

%files -n dotnet-nunit2-devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/nunit2.pc
