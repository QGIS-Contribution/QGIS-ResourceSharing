FROM qgis/qgis:release-3_22

ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /tmp/plugin
WORKDIR /tmp/plugin

COPY requirements requirements

RUN python3 -m pip install --no-cache-dir -U pip \
    && python3 -m pip install --no-cache-dir -U setuptools wheel \
    && python3 -m pip install --no-cache-dir -U -r requirements/testing.txt

RUN qgis --version
