#!/bin/bash
# Türkçe Piper ses modellerini (CC0 lisanslı) assets/voices klasörüne indirir.
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)/assets/voices"
mkdir -p "$DIR"
BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/tr/tr_TR"
for V in fettah fahrettin; do
  for EXT in onnx onnx.json; do
    F="$DIR/tr_TR-$V-medium.$EXT"
    [ -f "$F" ] || curl -L --fail -o "$F" "$BASE/$V/medium/tr_TR-$V-medium.$EXT" || {
      echo "HuggingFace erişilemedi, GitHub (sherpa-onnx) yedeğinden deneniyor..."
      TMP=$(mktemp -d)
      curl -L --fail -o "$TMP/v.tar.bz2" "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-$V-medium.tar.bz2"
      tar xjf "$TMP/v.tar.bz2" -C "$TMP"
      cp "$TMP"/vits-piper-tr_TR-$V-medium/tr_TR-$V-medium.onnx* "$DIR/"
      rm -rf "$TMP"
    }
  done
done
ls -la "$DIR"
