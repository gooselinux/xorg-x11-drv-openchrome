%define tarball xf86-video-openchrome
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define cvsdate xxxxxxx

%define with_xvmc 1
%define with_debug 0

Summary:	Xorg X11 openchrome video driver
Name:		xorg-x11-drv-openchrome
Version:	0.2.904
Release:	1%{?dist}
URL:		http://www.openchrome.org
License:	MIT
Group:		User Interface/X Hardware Support
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://www.openchrome.org/releases/%{tarball}-%{version}.tar.bz2
Source1:	openchrome.xinf

# Patches from upstream trunk :
# Fedora specific patches :
#Patch100:       openchrome-0.2.903-disable_hwcursor.patch
# Experimental patches (branch backport, etc...): 

ExclusiveArch:	%{ix86} x86_64

BuildRequires:	xorg-x11-server-devel
BuildRequires:	libX11-devel
BuildRequires:	libXext-devel
BuildRequires:	mesa-libGL-devel
%if %{with_xvmc}
BuildRequires:	libXvMC-devel
%endif
BuildRequires:	libdrm-devel >= 2.0-1
Requires:	xorg-x11-server-Xorg

Obsoletes:  xorg-x11-drv-via <= 0.2.2-4
Provides:   xorg-x11-drv-via = 0.2.2-5


%description 
X.Org X11 openchrome video driver.


%if %{with_xvmc}
%package devel
Summary:	Xorg X11 openchrome video driver XvMC development package
Group:		Development/System
Requires:	%{name} = %{version}-%{release}
Obsoletes:	xorg-x11-drv-via-devel <= 0.2.2-4
Provides:	xorg-x11-drv-via-devel = 0.2.2-5

%description devel
X.Org X11 openchrome video driver XvMC development package.
%endif


%prep
%setup -q -n %{tarball}-%{version}


%build
autoreconf -iv
%configure --disable-static --enable-dri \
%if %{with_debug}
           --enable-debug --enable-xv-debug
%endif

make


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases/openchrome.xinf

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ -e /etc/X11/xorg.conf ]; then
    sed -i "/Driver/s/via/openchrome/" /etc/X11/xorg.conf || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{driverdir}/openchrome_drv.so
%{_datadir}/hwdata/videoaliases/openchrome.xinf
%if %{with_xvmc}
%{_libdir}/libchromeXvMC.so.1
%{_libdir}/libchromeXvMC.so.1.0.0
%{_libdir}/libchromeXvMCPro.so.1
%{_libdir}/libchromeXvMCPro.so.1.0.0
%endif
%{_mandir}/man4/openchrome.4.gz

%if %{with_xvmc}
%files devel
%defattr(-,root,root,-)
%{_libdir}/libchromeXvMC.so
%{_libdir}/libchromeXvMCPro.so
%endif


%changelog
* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 0.2.904-1
- openchrome 0.2.904

* Fri Sep 18 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-16
- Update to latest snapshot (svn 789).
- Drop upstreamed patches.

* Tue Aug 25 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-15
- Add patch for resources/RAC API removal in xserver (RHBZ#516765).

* Thu Jul 30 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-14
- Update to latest snapshot (svn 766) for bugfixes.
- Drop upstreamed patches.
 
* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.903-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 18 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-12
- Update to latest snapshot (svn 758) :
  - Basic VX855 support.
  - Fix pci space corruption on P4M900 (RHBZ#506622).
  - Fix null pointer dereference in viaExaCheckComposite (RHBZ#449034).
- Add patch to allow 1200x900 panel (X0-1.5).
- Add patch to remove loader symbol lists, needed for xserver 1.7 (RHBZ#510206).
- Add experimental patch for better VT1625 support.
- Drop upstreamed patches.
 
* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 0.2.903-11.1
- ABI bump

* Thu Jun 18 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-11
- Update to latest snapshot (svn 751) :
  - Add support for VX800 integrated TMDS encoder.
  - Make sure Chrome9 chipsets use software rasterizer for 3D.
  - Various small fixes.
- Add patch for VX855 support.
- Add patch to fix cursor on secondary display.
- Add patch to disable TMDS by default.

* Sat Mar 21 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-10
- Update to latest snapshot (svn 740) :
  - Fix panel resolution detection fallback (RHBZ#491417).
  - Fix 2D engine initialization.
  - Add support for CX700 integrated TMDS encoder.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.903-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-8
- Update to latest snapshot (svn 735) :
  - Fix green bars after VT switch (RHBZ#469504).
  - Set P4M890 primary FIFO.

* Tue Feb 17 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-7
- Update to latest snapshot (svn 726) :
  - Bug fixes for XAA and EXA.
  - Fix 2d initialization for P4M900.

* Wed Jan 07 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-6
- Fix crash with xserver 1.6 (changeset 712) (RHBZ#479141).

* Mon Jan 05 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-5
- Update to latest snapshot (svn 711) :
  - Fix hardware cursor (RHBZ#465596).
  - Add VX800 Xv.

* Tue Dec 30 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-4
- Fix autoreconf call.

* Mon Dec 29 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-3
- Update to latest snapshot (svn 696), fix RHBZ#446489.
- Make debug build optional and disable it.

* Fri Nov 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-2
- Update to latest snapshot (svn 685), most notably add basic VX800 support.
- Turn on full debugging.

* Wed Aug 20 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-1
- Update to 0.2.903.

* Wed Aug 06 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-10
- Disable argb cursor for K8M800.

* Sun Aug 03 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-9
- New version of the panel and hw cursor patch.
- Rawhide is now using patch --fuzz=0, fixes for induced issues.

* Mon Jun 23 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-8
- New version of the panel and hw cursor patch.

* Sat May 31 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-7
- New panel and hardware cursor code from randr branch.

* Sun May 31 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-6
- Disable XvDMA for K8M890 and P4M890 (RHBZ #391621).

* Mon May 26 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-5
- Add patch to fix Xv on LCD for CX700.

* Sun May 25 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-4
- Unbreak ActiveDevice option.

* Thu Apr 17 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-3
- Strip leading /trunk/ from patch #2 and #3.

* Sun Apr 13 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-2
- Add patch to properly report driver version in the libpciaccess code path.
- Add patch to properly report chipset revision in the libpciaccess code path.

* Wed Apr 09 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-1
- New upstream release.
- Re-enable AGPDMA for K8M800 and VM800, as the drm bug is fixed in kernel
  >= 2.6.25rc7 (Patch #1).

* Mon Mar 17 2008 Jesse Keating <jkeating@redhat.com> - 0.2.901-16
- Remove dangerous unversioned obsoletes/provides.

* Sun Mar 16 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-15
- Update to latest svn snapshot (Rev. 553).

* Sun Mar 09 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-14
- Revert to last good version of the libpciaccess patch.

* Sun Mar 09 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-13
- Temporarily revert to old memory detection method. We need something that
  works out of the box for F9 Beta.

* Sat Mar 08 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-12
- Yet another revision of the libpciaccess patch.

* Fri Mar 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-11
- Fix a typo in libpciaccess patch.

* Fri Mar 07 2008 Adam Jackson <ajax@redhat.com> 0.2.901-10
- Fix -devel subpackage to obsolete via-devel properly.

* Thu Mar 06 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-9
- Fix libpciaccess patch.

* Thu Mar 06 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-8
- Add patch to fix XV on LCD for VM800.
- Improved libpciaccess patch.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.901-7
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-6
- Add patch to properly set fifo on P4M900.

* Fri Jan 19 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-5
- Add patch to replace xf86memcpy by plain memcpy.

* Thu Jan 10 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-4
- Another try at fixing the libpciaccess patch.

* Mon Jan 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-3
- And now fix patch filename...

* Mon Jan 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-2
- Fix broken libpciaccess patch.

* Wed Jan 02 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-1
- Update to 0.2.901.
- Remove obsoleted patches.
- Update libpciaccess patch.

* Fri Dec 08 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-9
- Add patch for preliminary libpciaccess support.

* Wed Nov 28 2007 Adam Jackson <ajax@redhat.com> 0.2.900-8
- Obsolete xorg-x11-drv-via.  The king is dead, long live the king.
- Munge xorg.conf in %%post to change from via to openchrome.
- Drive-by spec cleanups.

* Fri Nov 02 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-7
- Replace broken VT1625 NTSC patch.
- Add patch to announce as release not as development build.
- First official Fedora build.

* Thu Oct 18 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-6
- Update to official 0.2.900

* Wed Oct 10 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-5
- Update to release_0_3_0 branch rev. 410
- Add VT1625 patch for 720x576 PAL

* Mon Sep 10 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-4
- Update to release_0_3_0 branch rev. 384 plus all changes from experimental
  merged back
- Remove upstream patch #2

* Wed Aug 01 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-3
- Update to release_0_3_0 branch rev. 380 (fix a bug with XvMC acceleration)
- Add a patch to allow proper detection of DDR667 (patch #2)

* Mon Jul 16 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-2
- Update to release_0_3_0 branch rev. 373
- Add release notes to %%doc

* Thu Jul 05 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-1
- Initial build (release_0_3_0 branch rev. 365)
- Add some NTSC modes for the VT1625 (patch #1)
