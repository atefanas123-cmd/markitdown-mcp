FROM python:3.12-slim

RUN pip install --no-cache-dir markitdown-mcp

ENV PORT=10000

EXPOSE 10000

CMD sh -c "markitdown-mcp --http --host 0.0.0.0 --port ${PORT}"
