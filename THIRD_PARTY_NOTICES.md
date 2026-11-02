# Third-party components

Probably 4 is MIT licensed; see LICENSE. Third-party components retain their
own licenses. The Windows ZIP includes full texts in the `licenses` directory.

The packaging script copies license/notice files from the installed versions
of CustomTkinter, Pillow, darkdetect and packaging. Pillow's wheel notices
include its bundled image libraries. It also preserves available Python
runtime notices, the bundled Tk license, and copyright/name records from fonts.
Supplemental upstream texts and their sources are in `packaging/licenses`.

| Component | Notice location in ZIP |
| --- | --- |
| Python and standard library | licenses/Python.txt and licenses/python-runtime, when supplied |
| CustomTkinter and shapes font | licenses/customtkinter and font notice records |
| Pillow and its bundled codecs | licenses/pillow |
| darkdetect | licenses/darkdetect |
| packaging | licenses/packaging |
| Roboto fonts | licenses/Roboto.txt and Roboto font notice records |
| Tcl / Tk | licenses/tcl.txt and licenses/Tk.txt |
| OpenSSL, bzip2, Expat, libffi, liblzma, mpdecimal, zlib | corresponding supplemental texts in licenses |

The ZIP also includes Microsoft Visual C++ runtime DLLs delivered with the
Python distribution; these are Microsoft components, not MIT-licensed project
code. Their redistribution is governed by Microsoft's applicable runtime terms.
PyInstaller's bootloader exception permits distribution of the bundled app
under its own license: https://pyinstaller.org/en/stable/license.html.

CustomTkinter 6.0.0's metadata contains inconsistent license labels. Its actual
included LICENSE is MIT; that complete text is preserved without alteration.

When updating dependencies, review the new distribution's licenses, embedded
native libraries, and fonts. The collector checks that required notices exist;
it cannot decide every legal obligation or replace that review.
