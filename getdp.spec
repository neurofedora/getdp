Name:           getdp
Version:        2.7.0
Release:        1%{?dist}
Summary:        General Environment for the Treatment of Discrete Problems

License:        GPLv2+
URL:            http://www.geuz.org/getdp/
Source0:        http://www.geuz.org/getdp/src/%{name}-%{version}-source.tgz

BuildRequires:  cmake
BuildRequires:  gcc-c++ gcc-gfortran
BuildRequires:  arpack-devel
BuildRequires:  gmsh-devel
BuildRequires:  gsl-devel
BuildRequires:  lapack-devel blas-devel
BuildRequires:  python2-devel

%description
GetDP is an open source finite element solver using mixed elements to
discretize de Rham-type complexes in one, two and three dimensions. The main
feature of GetDP is the closeness between the input data defining discrete
problems (written by the user in ASCII data files) and the symbolic mathematical
expressions of these problems. 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{name}-%{version}-source

# remove bundled libs
rm -vrf contrib/

sed -i -e "/set(GETDP_LIB lib)/s/lib/%{_lib}/" CMakeLists.txt
# Force python 2.7
# https://geuz.org/trac/getdp/ticket/32
sed -i -e "/PythonLibs/s/)/ 2.7 REQUIRED)/" CMakeLists.txt

rm -rf build/
mkdir build/

%build
pushd build/
  %cmake ../ \
    -DENABLE_ARPACK=ON        \
    -DENABLE_BLAS_LAPACK=ON   \
    -DENABLE_FORTRAN=ON       \
    -DENABLE_GMSH=ON          \
    -DENABLE_GSL=ON           \
    -DENABLE_LEGACY=ON        \
    -DENABLE_MULTIHARMONIC=ON \
    -DENABLE_NR=OFF           \
    -DENABLE_NX=OFF           \
    -DENABLE_OCTAVE=OFF       \
    -DENABLE_OPENMP=ON        \
    -DENABLE_PETSC=OFF        \
    -DENABLE_PYTHON=ON        \
    -DENABLE_SLEPC=OFF        \
    -DENABLE_SPARSKIT=OFF     \
    -DENABLE_ZITSOL=OFF       \
    -DENABLE_BUILD_SHARED=ON  \
    -DENABLE_BUILD_DYNAMIC=ON
  %make_build
popd

%install
pushd build/
  %make_install
popd

# remove auto-installed docs
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%check
pushd build/
  ctest -VV
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license doc/LICENSE.txt
%doc doc/CREDITS.txt
%{_bindir}/%{name}
%{_libdir}/libGetDP.so.*
%{_mandir}/man1/%{name}.1*

%files devel
%doc demos
%{_includedir}/%{name}/
%{_libdir}/libGetDP.so

%changelog
* Sat Nov 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.7.0-1
- Initial package
