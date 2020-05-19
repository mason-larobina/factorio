for x in *.png; do
    prefix="${x%.png}"
    convert "${prefix}.png" -thumbnail '980>' "${prefix}.jpg"
done
