FROM python:3.11

RUN apt update && apt upgrade -y && \
    apt install -y git wget libxrender1 libxxf86vm1 libxfixes3 libxi6 libxkbcommon0 libsm6 libgl1 libgl1-mesa-glx

WORKDIR /hdRender
COPY hdRender/ .
RUN pip install -r requirements.txt

WORKDIR /
RUN wget https://mirror.clarkson.edu/blender/release/Blender4.3/blender-4.3.2-linux-x64.tar.xz && \
    tar -xf blender-4.3.2-linux-x64.tar.xz && \
    rm blender-4.3.2-linux-x64.tar.xz
# COPY blender-4.3.2-linux-x64/ ./blender-4.3.2-linux-x64

RUN pip install runpod

COPY rp_handler.py /

CMD ["python3", "-u", "rp_handler.py"]
