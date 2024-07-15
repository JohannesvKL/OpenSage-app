# This Dockerfile builds OpenMS on NuXL branch, the TOPP tools, pyOpenMS and thidparty tools.

# hints:
# build image and give it a name (here: streamlitapp) with: docker build --no-cache -t streamlitapp:latest --build-arg GITHUB_TOKEN=<your-github-token> . 2>&1 | tee build.log 
# check if image was build: docker image ls
# run container: docker run -p 8501:8501 streamlitappsimple:latest
# debug container after build (comment out ENTRYPOINT) and run container with interactive /bin/bash shell
# prune unused images/etc. to free disc space (e.g. might be needed on gitpod). Use with care.: docker system prune --all --force

# Use an ARM64-compatible base image
#FROM --platform=linux/arm64 ubuntu:22.04 AS setup-build-system

# Use an ARM64-compatible base image
#Try doing it platform independent next 
#FROM --platform=linux/arm64 ubuntu:22.04 AS setup-build-system
FROM ubuntu:22.04 AS setup-build-system

ARG OPENMS_REPO=https://github.com/JohannesvKL/OpenMSOpenSageSearch
ARG OPENMS_BRANCH=OpenSageSearch
ARG GITHUB_TOKEN
ARG PORT=8501

USER root

# Install required Ubuntu packages
RUN apt-get -y update && apt-get install -y --no-install-recommends --no-install-suggests \
    g++ autoconf automake patch libtool make git gpg wget ca-certificates curl \
    libsvm-dev libeigen3-dev coinor-libcbc-dev libglpk-dev libzip-dev zlib1g-dev \
    libxerces-c-dev libbz2-dev libomp-dev libhdf5-dev \
    libboost-date-time1.74-dev libboost-iostreams1.74-dev libboost-regex1.74-dev \
    libboost-math1.74-dev libboost-random1.74-dev \
    qtbase5-dev libqt5svg5-dev libqt5opengl5-dev \
    rustc cargo \
    && rm -rf /var/lib/apt/lists/*

# Download and install mamba for ARM64
ENV PATH="/root/mambaforge/bin:${PATH}"
RUN wget -q https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-aarch64.sh \
    && bash Mambaforge-Linux-aarch64.sh -b \
    && rm -f Mambaforge-Linux-aarch64.sh

# Setup mamba environment
COPY environment.yml ./environment.yml
RUN mamba env create -f environment.yml 
SHELL ["mamba", "run", "-n", "streamlit-env", "/bin/bash", "-c"]

# Install up-to-date cmake via mamba and packages for pyOpenMS build
RUN mamba install cmake \
    && pip install setuptools nose Cython autowrap pandas numpy pytest\
    && pip install --force-reinstall numpy==1.26.4  \
    && pip install captcha 



# Clone OpenMS branch and the associated contrib+thirdparties+pyOpenMS-doc submodules
RUN git clone --recursive --depth=1 -b ${OPENMS_BRANCH} --single-branch ${OPENMS_REPO} /OpenMS

WORKDIR /OpenMS
RUN git submodule update --init THIRDPARTY

# Create thirdparty directory and copy files
RUN mkdir /thirdparty && \
    cp -r THIRDPARTY/All/* /thirdparty && \
    cp -r THIRDPARTY/Linux/64bit/* /thirdparty && \
    chmod -R +x /thirdparty

# Set the PATH for third-party tools
ENV PATH="/thirdparty/LuciPHOr2:/thirdparty/MSGFPlus:/thirdparty/Sirius:/thirdparty/ThermoRawFileParser:/thirdparty/Comet:/thirdparty/Fido:/thirdparty/MaRaCluster:/thirdparty/MyriMatch:/thirdparty/OMSSA:/thirdparty/Percolator:/thirdparty/SpectraST:/thirdparty/XTandem:/thirdparty/crux:${PATH}"

# Clone and build Sage
RUN git clone https://github.com/lazear/sage /sage
WORKDIR /sage
RUN cargo build --release
ENV PATH="/sage/target/release:${PATH}"

# Build OpenMS and pyOpenMS
FROM setup-build-system AS compile-openms
WORKDIR /openms-build

# Configure
RUN cmake -DCMAKE_BUILD_TYPE='Release' \
          -DCMAKE_PREFIX_PATH='/OpenMS/contrib-build/;/usr/;/usr/local' \
          -DHAS_XSERVER=OFF -DBOOST_USE_STATIC=OFF -DPYOPENMS=ON \
          -DPY_MEMLEAK_DISABLE=On ../OpenMS

# Build TOPP tools and pyOpenMS
RUN make -j4 TOPP
#RUN make -j4 pyopenms

#RUN pip install boost 
#RUN pip install pyopenms

# Install pyOpenMS
#WORKDIR /openms-build/pyOpenMS
#RUN pip install dist/*.whl

# Prepare OpenMS directories
WORKDIR /
RUN mkdir /openms && \
    cp -r /openms-build/bin /openms/bin && \
    cp -r /openms-build/lib /openms/lib && \
    cp -r /OpenMS/share/OpenMS /openms/share && \
    rm -rf /OpenMS /openms-build

# Set environment variables
ENV PATH="/openms/bin/:${PATH}"
ENV LD_LIBRARY_PATH="/openms/lib/:${LD_LIBRARY_PATH}"
ENV OPENMS_DATA_PATH="/openms/share/"

# Prepare and run streamlit app
FROM compile-openms AS run-app
WORKDIR /app

# Copy Streamlit app files
COPY app.py /app/
COPY src/ /app/src/
COPY assets/ /app/assets/
COPY example-data/ /app/example-data/
COPY pages/ /app/pages/
COPY .streamlit/config.toml /app/.streamlit/

# Copy Sage binary
COPY --from=compile-openms /sage/target/release/sage /usr/local/bin/

EXPOSE ${PORT}

# Run Streamlit app
CMD ["mamba", "run", "--no-capture-output", "-n", "streamlit-env", "streamlit", "run", "app.py"]