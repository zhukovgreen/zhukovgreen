set -ex

for FILE in "$@"
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
done

python3 scripts/commit_updated_files.py