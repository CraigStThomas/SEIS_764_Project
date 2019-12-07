#!/bin/bash

shopt -s globstar

for file in ./A01/**; do 
    if [[ -f "$file" ]]; then
        dirname="${file%/*}/"
        basename="${file:${#dirname}}"
        n=$(printf %03d "$basename" | cut -d '_' -f 1)
        convert 'A01/'$basename -resize 120 'A01/'$n'_compressed.png'
    fi
done

mkdir A01_compressed
mv A01/*_compressed.png A01_compressed/

for file in ./A02/**; do 
    if [[ -f "$file" ]]; then
        dirname="${file%/*}/"
        basename="${file:${#dirname}}"
        n=$(printf %03d "$basename" | cut -d '_' -f 1)
        convert 'A02/'$basename -resize 120 'A02/'$n'_compressed.png'
    fi
done

mkdir A02_compressed
mv A02/*_compressed.png A02_compressed/

for file in ./A03/**; do 
    if [[ -f "$file" ]]; then
        dirname="${file%/*}/"
        basename="${file:${#dirname}}"
        n=$(printf %03d "$basename" | cut -d '_' -f 1)
        convert 'A03/'$basename -resize 120 'A03/'$n'_compressed.png'
    fi
done

mkdir A03_compressed
mv A03/*_compressed.png A03_compressed/

for file in ./A04/**; do 
    if [[ -f "$file" ]]; then
        dirname="${file%/*}/"
        basename="${file:${#dirname}}"
        n=$(printf %03d "$basename" | cut -d '_' -f 1)
        convert 'A04/'$basename -resize 120 'A04/'$n'_compressed.png'
    fi
done

mkdir A04_compressed
mv A04/*_compressed.png A04_compressed/

for file in ./A05/**; do 
    if [[ -f "$file" ]]; then
        dirname="${file%/*}/"
        basename="${file:${#dirname}}"
        n=$(printf %03d "$basename" | cut -d '_' -f 1)
        convert 'A05/'$basename -resize 120 'A05/'$n'_compressed.png'
    fi
done

mkdir A05_compressed
mv A05/*_compressed.png A05_compressed/

for file in ./A06/**; do 
    if [[ -f "$file" ]]; then
        dirname="${file%/*}/"
        basename="${file:${#dirname}}"
        n=$(printf %03d "$basename" | cut -d '_' -f 1)
        convert 'A06/'$basename -resize 120 'A06/'$n'_compressed.png'
    fi
done

mkdir A06_compressed
mv A06/*_compressed.png A06_compressed/
