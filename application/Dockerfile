FROM python:3.8.2-slim as builder

WORKDIR /home/app

RUN apt update && \
    apt install -y gcc libpq-dev python3-dev && \
    python3.8 -m pip install --upgrade pip

COPY requirements.txt .
RUN python3.8 -m pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY . .
RUN python3.8 setup.py bdist_wheel -d /usr/src/app/wheels

# ================================================================================================= #
#                                       END BUILDER
# ================================================================================================= #

FROM python:3.8.2-slim

# create directory for the app user
WORKDIR /home/app

COPY --from=builder /usr/src/app/wheels /wheels
# COPY --from=builder /usr/src/app/requirements.txt .

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install --no-cache /wheels/*

RUN apt update && \
    apt install -y gcc libpq-dev python3-dev

# create the app user
RUN groupadd app
RUN useradd -g app app

# chown all the files to the app user
RUN chown -Rf app:app /home/app

# change to the app user
USER app

RUN pip freeze
COPY config /home/src/config
EXPOSE 8080
CMD ["gunicorn", "--config", "/home/src/config/gunicorn.conf.py", "facturas_back.app:start_server()"]
