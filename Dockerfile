FROM python:3.11-slim

# Set working directory
WORKDIR /app

# ── System deps ────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        curl \
        ca-certificates \
        ffmpeg \
        libicu-dev \
        libssl-dev \
        libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# ── N_m3u8DL-RE binary ────────────────────────────────────────────────────
# Downloads the official release tarball, extracts, installs to PATH.
RUN wget -q \
        https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.5.1-beta/N_m3u8DL-RE_v0.5.1-beta_linux-x64_20251029.tar.gz \
        -O /tmp/nm3u8dl.tar.gz \
    && tar -xzf /tmp/nm3u8dl.tar.gz -C /tmp/ \
    && find /tmp -name "N_m3u8DL-RE" -type f -exec mv {} /usr/local/bin/N_m3u8DL-RE \; \
    && chmod +x /usr/local/bin/N_m3u8DL-RE \
    && rm -rf /tmp/nm3u8dl.tar.gz /tmp/N_m3u8DL-RE* \
    # Smoke-test: print version; fail build early if binary is broken
    && N_m3u8DL-RE --version || true

# ── Python dependencies ────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application code ───────────────────────────────────────────────────────
COPY . .

# ── Downloads directory ────────────────────────────────────────────────────
RUN mkdir -p /tmp/downloads
ENV DOWNLOAD_DIR=/tmp/downloads

# ── Run the bot ────────────────────────────────────────────────────────────
CMD ["python", "bot.py"]
