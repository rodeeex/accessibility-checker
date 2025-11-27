import os
import sys
import subprocess
from pathlib import Path

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

python_exe = sys.executable
browser_path = run_cmd(f'"{python_exe}" -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); print(p.chromium.executable_path); p.stop()"')
browser_dir = str(Path(browser_path).parent.parent)
browser_ver = Path(browser_dir).name

try:
    import playwright_stealth
    stealth_dir = Path(playwright_stealth.__file__).parent
    stealth_js_src = str(stealth_dir / "js")
    stealth_js_dst = "playwright_stealth/js"
except ImportError:
    stealth_js_src = None
    stealth_js_dst = None

if stealth_js_src:
    print(f"playwright_stealth/js: {stealth_js_src}")

datas = []
binaries = []

binaries.append((os.path.join(browser_dir, "**"), f"playwright/driver/package/.local-browsers/{browser_ver}"))

if stealth_js_src and os.path.isdir(stealth_js_src):
    datas.append((os.path.join(stealth_js_src, "*"), stealth_js_dst))

if os.path.isdir("rules"):
    datas.append(("rules/*", "rules"))

if os.path.isdir("report_maker"):
    datas.append(("report_maker/*", "report_maker"))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'playwright',
        'playwright.sync_api',
        'playwright._impl',
        'playwright._impl._driver',
        'bs4',
        'lxml',
        'weasyprint',
        'colorama',
        'playwright_stealth',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

exe = EXE(
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='accessibility-checker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

pyz = PYZ(a.pure)

exe_onefile = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='accessibility-checker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    append_pkg=True,
)