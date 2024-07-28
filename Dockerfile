# Official Python runtime as a parent image
FROM python:3

# Install dependencies and Jupyter
RUN pip install numpy matplotlib jupyter

# Install latex
RUN apt-get update -y \
    && apt-get install texlive-science -y \
    && apt-get install dvipng texlive-latex-extra texlive-fonts-recommended cm-super -y

# Create `dev` user with privileged access
RUN apt-get install -y sudo \
    && useradd -m -s /bin/bash dev \
    && usermod -aG sudo dev \
    && echo "dev ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/dev

# Make port 8888 available for possible jupyter server
EXPOSE 8888

USER dev
WORKDIR /home/dev

CMD ["bash"]