!include "MUI2.nsh"

Name "TinForge v2"
OutFile "TinForge-v2-Setup.exe"
InstallDir "$PROGRAMFILES\\TinForge v2"
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\\..\\..\\resources\\licenses\\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  File /r "..\\..\\..\\dist\\tinforge-v2\\*"

  CreateDirectory "$SMPROGRAMS\\TinForge v2"
  CreateShortcut "$DESKTOP\\TinForge v2.lnk" "$INSTDIR\\tinforge-v2.exe"
  CreateShortcut "$SMPROGRAMS\\TinForge v2\\TinForge v2.lnk" "$INSTDIR\\tinforge-v2.exe"

  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\TinForge v2" "DisplayName" "TinForge v2"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\TinForge v2" "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\\TinForge v2.lnk"
  Delete "$SMPROGRAMS\\TinForge v2\\TinForge v2.lnk"
  RMDir "$SMPROGRAMS\\TinForge v2"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\TinForge v2"
SectionEnd
