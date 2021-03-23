apt-get install -y gdb gdbserver binutils python3 ruby git tmux ssh python3-pip
gem install one_gadget
mkdir /home/pwn && chmod -R 777 /home/pwn
cd /home/pwn
python3 -m pip install virtualenv
virtualenv .
/bin/bash -c 'source /home/pwn/bin/activate'
python3 -m pip install pwntools
git clone https://github.com/pwndbg/pwndbg
cd pwndbg && ./setup.sh
