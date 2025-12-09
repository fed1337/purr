FROM python:3.10-slim-bookworm AS builder

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install build dependencies
RUN apt update && apt upgrade -y && apt install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    libldap2-dev \
    libsasl2-dev && \
    rm -rf /var/lib/apt/lists/*

# Install nodejs 18 with npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt update && \
    apt install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed uv binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy dependency files & set workdir
WORKDIR /opt/lemur
COPY . .

# Install Python dependencies with uv
RUN uv sync --frozen

RUN npm install \
    && npm run build_static \
    && node_modules/.bin/gulp package --urlContextPath="" \
    && rm -rf node_modules bower_components .tmp


FROM python:3.10-slim-bookworm AS runtime

ENV PATH="/opt/lemur/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt update && apt upgrade -y && apt install -y --no-install-recommends \
    debian-keyring debian-archive-keyring apt-transport-https curl libldap-2.5-0 make gnupg && \
    rm -rf /var/lib/apt/lists/*

RUN curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/gpg.key | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg && \
    curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt | tee /etc/apt/sources.list.d/caddy-stable.list && \
    chmod o+r /usr/share/keyrings/caddy-stable-archive-keyring.gpg && \
    chmod o+r /etc/apt/sources.list.d/caddy-stable.list && \
    apt update && apt install caddy && \
    rm -rf /var/lib/apt/lists/*

# Create lemur user
RUN useradd --create-home --shell /bin/bash lemur

# Copy built project
COPY --from=builder --chown=lemur:lemur /opt/lemur /opt/lemur

# Ensure entrypoint is executable
RUN chmod +x /opt/lemur/entrypoint

# Switch to the user
USER lemur

# Expose port
EXPOSE 80

# Default command
ENTRYPOINT ["/opt/lemur/entrypoint"]
