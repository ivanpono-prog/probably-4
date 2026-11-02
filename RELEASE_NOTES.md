# Probably 4 v1.0.1 — release candidate

Packaging and distribution improvements:

- Windows build recipe and locked PyInstaller dependency.
- Product/version information in Probably4.exe.
- Project license and collected third-party notices in the ZIP.
- SHA256 for the ZIP and a manifest of bundled files.
- Build information linking the package to its source commit and dependency lock.
- Automated Windows build and extracted-EXE smoke check.

Download `Probably4-v1.0.1-win64.zip`, extract the entire archive, and launch
`Probably4/Probably4.exe`. Keep `_internal` and the license files with the EXE.
No separate Python installation is required. This candidate is unsigned.

Manual validation on a clean Windows 10/11 x64 installation is pending.
Replace this sentence with the actual tested OS builds/results before publishing.
The automated runner is Windows Server 2025; it is not evidence of manual
testing on desktop Windows. No Windows 7, 32-bit or native ARM64 build is offered.

Verify the download against the separately attached `.sha256` file:

```powershell
Get-FileHash .\Probably4-v1.0.1-win64.zip -Algorithm SHA256
```

Compare all 64 hexadecimal characters. A matching hash checks integrity; it
does not provide a publisher signature.
