#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$APP_ROOT"
export COPYFILE_DISABLE=1
python3 "$SCRIPT_DIR/generate_icon.py" >/dev/null
rm -rf build dist
python3 setup.py py2app
cp "$APP_ROOT/assets/study-helper-icon.png" "$APP_ROOT/dist/Syllabus.app/Contents/Resources/study-helper-icon.png"
xattr -cr "$APP_ROOT/dist/Syllabus.app" 2>/dev/null || true
/usr/libexec/PlistBuddy -c "Set :CFBundleIconFile study-helper-icon.png" "$APP_ROOT/dist/Syllabus.app/Contents/Info.plist" >/dev/null 2>&1 || true
codesign --force --deep --sign - "$APP_ROOT/dist/Syllabus.app" >/dev/null 2>&1 || true
echo "$APP_ROOT/dist/Syllabus.app"
