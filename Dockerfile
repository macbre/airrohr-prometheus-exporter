FROM python:3-alpine
WORKDIR /opt/airrohr-prometheus-exporter

# install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt && python -V && pip list

# set up env
ENV FLASK_DEBUG 0
ENV FLASK_ENV production
ENV HTTP_PORT 8888
EXPOSE 8888

# copy the rest of the app and run it
USER nobody
COPY . .

# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=15s --timeout=1s --retries=3 \
  CMD wget 0.0.0.0:${HTTP_PORT} --spider -q -U 'wget/healthcheck' || exit 1

CMD ["sh", "server.sh"]
