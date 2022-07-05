# Separate build image
FROM python:3.9-slim-buster as compile-image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
COPY /lib/ opt/venv/lib/python3.9/site-packages/
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:3.9-slim-buster
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /usr/src/app/
COPY ./ /usr/src/app/
ENTRYPOINT ["python", "-m", "main.py"]