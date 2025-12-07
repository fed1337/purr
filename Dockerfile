FROM python:3.10-slim-bookworm AS builder

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
    && rm -rf node_modules bower_components .tmp


FROM python:3.10-slim-bookworm AS runtime

ENV PATH="/opt/lemur/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt update && apt upgrade -y && apt install -y --no-install-recommends \
    curl \
    libldap-2.5-0 \
    make && \
    rm -rf /var/lib/apt/lists/*

# Create lemur user
RUN useradd --create-home --shell /bin/bash lemur

# Copy built project
COPY --from=builder /opt/lemur /opt/lemur

# Ensure entrypoint is executable
RUN chmod +x /opt/lemur/entrypoint

# Permissions
RUN chown -R lemur:lemur /opt/lemur

# Switch to user
USER lemur

# Expose port
EXPOSE 8000

# Default command
ENTRYPOINT ["/opt/lemur/entrypoint"]
CMD ["start"]
