FROM python:3.12-slim

ARG POETRY_INSTALL_PATH=/opt/poetry

WORKDIR /app

# 必要最小限のシステムパッケージをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetry のインストール
ENV POETRY_HOME=${POETRY_INSTALL_PATH} \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.8.3 \
    PATH="${POETRY_INSTALL_PATH}/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

# 依存関係ファイルのコピーとインストール
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

# アプリケーションのコピー
COPY . .

# 実行ユーザーの作成とパーミッション設定
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

# アプリケーションの実行
CMD ["poetry", "run", "python", "-m", "app.cmd.main"]
