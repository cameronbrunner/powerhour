FROM python:3 as builder
RUN apt-get update && \
apt-get install -y build-essential python3-pip python3-dev python3-smbus git
RUN pip install wheel build

FROM builder as lib3relind
RUN git clone https://github.com/SequentMicrosystems/3relind-rpi.git
WORKDIR 3relind-rpi/python/3relind/
RUN python3 -m build

FROM builder as smbus
RUN pip wheel smbus

FROM python:3-slim
COPY --from=lib3relind /3relind-rpi/python/3relind/dist/lib3relind-1.0.0-py3-none-any.whl .
COPY --from=smbus smbus-1.1.post2-cp313-cp313-linux_aarch64.whl .
RUN pip install synochat flask minimalmodbus \
    ./lib3relind-1.0.0-py3-none-any.whl \
    smbus-1.1.post2-cp313-cp313-linux_aarch64.whl
EXPOSE 5001
ADD powerhour.py .
CMD python3 powerhour.py
