set -ex

for FILE in *.md
do
   case "$FILE" in
   *.md)
     ;;
   *)
     >&2 echo "$FILE should have .md ext"; exit 2
     ;;
   esac
   vim -E -s -c "runtime syntax/2html.vim" -c wqa \
   "$FILE" && weasyprint -s pdfstyle.css \
   "$FILE.html" "$FILE.pdf"
   rm "$FILE.html"
done

cat ./artem_cv.md > README.md
poetry run python scripts/commit_updated_files.py
echo "\n\nAll jobs done successfully!\n\n"
