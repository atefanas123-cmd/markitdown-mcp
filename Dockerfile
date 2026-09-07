FROM python:3.12-slim

RUN pip install --no-cache-dir "markdown-mcp" "mcp>=1.28,<2"

ENV PORT=10000

EXPOSE 10000

CMD sh -c "markdown-mcp --http --host 0.0.0.0 --port $PORT"
