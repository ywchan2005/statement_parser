##############################
# dev
##############################

FROM python:3.9-bookworm AS dev

RUN apt-get update \
  && apt-get install -y libgl1-mesa-glx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY .config /root/.config

RUN pip install pdfquery six scipy pandas gspread

WORKDIR /app
