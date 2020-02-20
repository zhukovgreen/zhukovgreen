FROM thinca/vim:latest-full as base
RUN apk --update --upgrade add gcc \
    fontconfig \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev \
    cairo-dev \
    pango-dev \
    openssl-dev \
    git \
    gdk-pixbuf-dev
RUN pip3 install weasyprint
RUN pip3 install poetry
WORKDIR "/source"
COPY pyproject.toml poetry.lock /source/
RUN poetry install
FROM base as setup
COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]
