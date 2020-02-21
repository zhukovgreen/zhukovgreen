FROM thinca/vim:latest-full as base
RUN apk --update --upgrade add gcc \
    ttf-dejavu \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev \
    cairo-dev \
    pango-dev \
    openssl-dev \
    git \
    fontconfig \
    ca-certificates \
    py3-lxml \
    gdk-pixbuf
RUN pip3 install poetry
WORKDIR "/source"
COPY pyproject.toml poetry.lock /source/
RUN poetry install
FROM base as setup
COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]
