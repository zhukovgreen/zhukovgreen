set -ex

CV="./docs/artem_cv.md"

if [ $# -eq 0 ]
  then
    vim -E -s \
    -c "syntax on" \
    -c "let g:html_no_progres=1" \
    -c "runtime syntax/2html.vim" \
    -c wqa "$CV" && weasyprint -s pdfstyle.css \
    "$CV.html" "$CV.pdf"
    rm "$CV.html"
    cat "$CV" > "./README.md"
    poetry run python scripts/commit_updated_files.py
    echo "\n\nAll jobs done successfully!\n\n"
fi

exec "$@"