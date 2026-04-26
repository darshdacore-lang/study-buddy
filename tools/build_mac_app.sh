#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MAC_DIR="$APP_ROOT/mac"
BUNDLE="$MAC_DIR/Syllabus.app"
ICONSET="$MAC_DIR/study-helper.iconset"
ICON_PNG="$APP_ROOT/assets/study-helper-icon.png"

python3 "$SCRIPT_DIR/generate_icon.py"

mkdir -p "$BUNDLE/Contents/MacOS" "$BUNDLE/Contents/Resources" "$ICONSET"
chmod +x "$BUNDLE/Contents/MacOS/syllabus"
cp "$ICON_PNG" "$BUNDLE/Contents/Resources/study-helper-icon.png"

rm -rf "$ICONSET"
mkdir -p "$ICONSET"

sips -z 16 16 "$ICON_PNG" --out "$ICONSET/icon_16x16.png" >/dev/null
sips -z 32 32 "$ICON_PNG" --out "$ICONSET/icon_16x16@2x.png" >/dev/null
sips -z 32 32 "$ICON_PNG" --out "$ICONSET/icon_32x32.png" >/dev/null
sips -z 64 64 "$ICON_PNG" --out "$ICONSET/icon_32x32@2x.png" >/dev/null
sips -z 128 128 "$ICON_PNG" --out "$ICONSET/icon_128x128.png" >/dev/null
sips -z 256 256 "$ICON_PNG" --out "$ICONSET/icon_128x128@2x.png" >/dev/null
sips -z 256 256 "$ICON_PNG" --out "$ICONSET/icon_256x256.png" >/dev/null
sips -z 512 512 "$ICON_PNG" --out "$ICONSET/icon_256x256@2x.png" >/dev/null
sips -z 512 512 "$ICON_PNG" --out "$ICONSET/icon_512x512.png" >/dev/null
sips -z 1024 1024 "$ICON_PNG" --out "$ICONSET/icon_512x512@2x.png" >/dev/null

if iconutil -c icns "$ICONSET" -o "$BUNDLE/Contents/Resources/study-helper.icns" 2>/dev/null; then
  /usr/libexec/PlistBuddy -c "Set :CFBundleIconFile study-helper.icns" "$BUNDLE/Contents/Info.plist" >/dev/null
else
  /usr/libexec/PlistBuddy -c "Set :CFBundleIconFile study-helper-icon.png" "$BUNDLE/Contents/Info.plist" >/dev/null
fi

echo "$BUNDLE"
