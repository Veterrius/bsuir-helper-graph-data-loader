FROM astral/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv pip install . --system --no-cache

FROM astral/uv:python3.13-bookworm-slim AS final

WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN useradd --create-home --shell /bin/bash appuser
COPY --from=builder /usr/local/ /usr/local/
ENV PYTHONPATH="/app/src"

COPY ./src ./src

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "bsuir_helper_graph_data_loader.__main__:app", "--host", "0.0.0.0", "--port", "8000"]