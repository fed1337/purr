FROM python:3.10-alpine3.22 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /bin/

ENV PATH="/root/.local/bin/:$PATH" \
    CFLAGS="-Os -fomit-frame-pointer" \
    LDFLAGS="-Wl,--strip-all"

WORKDIR /opt/lemur
COPY . .

RUN apk add --update --no-cache --virtual build-dependencies \
    curl \
    bash \
    git \
    tar \
    musl-dev \
    gcc \
    openldap-dev \
    binutils \
    npm \
    && uv sync --no-dev --frozen --compile-bytecode

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSL https://github.com/caddyserver/caddy/releases/download/v2.10.2/caddy_2.10.2_linux_amd64.tar.gz | tar xz -C /usr/bin \
    && npm config set cache /tmp/npm-cache \
    && npm install \
    && node_modules/.bin/gulp build \
    && node_modules/.bin/gulp package --urlContextPath="" \
    && rm -rf node_modules bower_components .tmp /tmp/npm-cache \
    /usr/lib/python3.10/ensurepip \
    /usr/lib/python3.10/idlelib \
    /usr/lib/python3.10/test \
    /usr/lib/python3.10/lib2to3 \
    /usr/lib/python3.10/pydoc_data \
    /usr/lib/python3.10/tkinter \
    && strip /usr/bin/caddy \
    && strip /opt/lemur/.venv/lib/python*/site-packages/**/*.so || true \
    && find /opt/lemur/.venv -name "*.so" -exec strip --strip-unneeded {} + || true \
    && apk del build-dependencies


FROM python:3.10-alpine3.22 AS runtime

ENV uid=1337
ENV gid=1337
ENV user=lemur
ENV group=lemur

ENV PATH="/opt/lemur/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache curl libldap bash openssl

RUN addgroup -S ${group} -g ${gid} \
    && adduser -D -S ${user} -G ${group} -u ${uid}

COPY --from=builder --chown=${uid}:${gid} /opt/lemur /opt/lemur
COPY --from=builder --chown=${uid}:${gid} /usr/bin/caddy /usr/bin/caddy

RUN chmod +x /opt/lemur/docker/entrypoint.sh

USER lemur

EXPOSE 80

ENTRYPOINT ["/opt/lemur/docker/entrypoint.sh"]
