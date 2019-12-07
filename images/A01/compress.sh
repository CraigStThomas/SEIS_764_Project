#!/bin/bash

shopt -s globstar

for file in ./**; do 
    if [[ -f "$file" ]]; then
        dirname="${file%/*}/"
        basename="${file:${#dirname}}"
        echo mv "$file" "$dirname${basename%.*}_$basename"
        n=$(printf %03d "$basename" | cut -d '_' -f 1)
        convert "$basename" -resize 120 $n'_compressed.png'

    fi
done

echo 'someletters_12345_moreleters.ext' | cut -d'_' -f 1
convert 0_A01_blended.png -resize 240 0_compressed.png
