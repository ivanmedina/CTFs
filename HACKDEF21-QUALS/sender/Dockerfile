FROM ubuntu:20.10

RUN apt-get update && apt-get install -y socat

RUN adduser --no-create-home --disabled-password --gecos "" ctf
WORKDIR /home/ctf

COPY --chown=root:ctf bin/pwn_300 bin/flag.txt ./
RUN chmod 2750 pwn_300 && \
    chmod 640 flag.txt 

USER ctf
CMD ["socat", "tcp-listen:1335,fork,reuseaddr", "exec:./pwn_300"]

EXPOSE 1335
