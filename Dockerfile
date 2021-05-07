FROM python:3.8-slim

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PIP_NO_CACHE_DIR=off
RUN apt update
COPY ./check_hashes.py /app/check_hashes.py
WORKDIR /out/
ENTRYPOINT [ "python3","/app/check_hashes.py"]
