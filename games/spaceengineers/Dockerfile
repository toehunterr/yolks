# ---------------------------------------
# Generic Wine image based on Wine stable
# ---------------------------------------
    FROM            ghcr.io/ptero-eggs/yolks:debian

    ## install required packages
    RUN             dpkg --add-architecture i386 \
                    && apt update -y \
                    && apt install -y --no-install-recommends gnupg2 numactl tzdata software-properties-common libntlm0 winbind xvfb xauth python3 xmlstarlet libncurses5:i386 libncurses6:i386 libsdl2-2.0-0 libsdl2-2.0-0:i386 dos2unix
    
    RUN             cd /tmp/ \
                    && curl -sSL https://github.com/gorcon/rcon-cli/releases/download/v0.10.3/rcon-0.10.3-amd64_linux.tar.gz > rcon.tar.gz \
                    && tar xvf rcon.tar.gz \
                    && mv rcon-0.10.3-amd64_linux/rcon /usr/local/bin/
    
    # Install wine and with recommends
    RUN             mkdir -pm755 /etc/apt/keyrings
    RUN             wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
    RUN             wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources
    RUN             apt update
    RUN             apt install --install-recommends winehq-stable cabextract wine-binfmt -y
    
    # Set up Winetricks and install Visual C++ Redistributable
    RUN             wget -q -O /usr/sbin/winetricks https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks \
                    && chmod +x /usr/sbin/winetricks
    
    COPY            ./config_parser.py /config_parser.py
    RUN             chown container:container /config_parser.py && chmod +x /config_parser.py
    COPY            ./../entrypoint.sh /entrypoint.sh    
    
    ENV             HOME=/home/container
    ENV             WINEPREFIX=/home/container/.wine
    ENV             WINEDLLOVERRIDES="mscoree,mshtml="
    ENV             DISPLAY=:0
    ENV             DISPLAY_WIDTH=1024
    ENV             DISPLAY_HEIGHT=768
    ENV             DISPLAY_DEPTH=16
    ENV             AUTO_UPDATE=1
    ENV             XVFB=1
    
    CMD             [ "/bin/bash", "/entrypoint.sh" ]