FROM thinca/vim as base
RUN apk --update --upgrade add gcc \
    fontconfig \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev
RUN pip3 install weasyprint
FROM base as setup
WORKDIR "/source"
COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["artem_cl.md", "artem_cv.md"]
