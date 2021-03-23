FROM ubuntu:disco-20200114
MAINTAINER Lys

RUN sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy xinetd
RUN useradd -m babystack
RUN chown -R root:root /home/babystack
RUN chmod -R 755 /home/babystack
#ENTRYPOINT ["sh"]


RUN apt-get install -y gdb gdbserver binutils python3 ruby git tmux ssh python3-pip python2.7 python-pip vim
RUN gem install one_gadget
RUN mkdir /home/pwn
RUN chmod -R 777 /home/pwn
RUN python3 -m pip install virtualenv
RUN virtualenv /home/pwn
RUN /bin/bash -c 'source /home/pwn/bin/activate'
#python3 -m pip install pwntools 
RUN git clone https://github.com/pwndbg/pwndbg && \
cd pwndbg && ./setup.sh

#RUN echo 0 > /proc/sys/kernel/randomize_va_space

CMD ["/usr/sbin/xinetd","-dontfork"]



#CMD ["/home/babystack/docker-entrypoint.sh"]

