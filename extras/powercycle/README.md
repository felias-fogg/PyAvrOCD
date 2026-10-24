# Power-cycling the target through the laboratory supply

`spd3303x.py` talks to a Siglent SPD3303X over SCPI: power-cycle, switch, read the status.
`supplyctl.py` is the gateway in front of it. The supply sits on a private link of a Raspberry Pi,
so no other machine can reach it, and the development machine gets exactly four requests through
SSH, each checked by the gateway:

    ssh supplyctl cycle 1          power-cycle CH1 (optionally: cycle 1 2.5, at most 10 s off)
    ssh supplyctl on 1             switch CH1 on
    ssh supplyctl off 1            switch CH1 off
    ssh supplyctl status 1         state, setpoints, measured voltage and current

Setpoints are never changed. Before an output is switched on, the gateway reads them and refuses if
one is above the ceiling configured on the Pi, so a supply misconfigured by hand is not switched on
either. The current limit set on the front panel stays the protection that does not depend on any
software.

    Mac ──LAN──► Pi (WiFi) ──eth0, 10.33.0.0/24──► supply 10.33.0.2

## 1. The private link

On the supply, in the LAN settings on the front panel: DHCP off, IP `10.33.0.2`, mask
`255.255.255.0`, no gateway. Then the network cable goes from the supply to the Pi's Ethernet port and nowhere else.
The Pi itself has to be on the LAN through WiFi; move it there first if it is wired now.

On the Pi:

    sudo nmcli con add type ethernet ifname eth0 con-name supply \
         ipv4.method manual ipv4.addresses 10.33.0.1/24 ipv4.never-default yes ipv6.method disabled
    sudo nmcli con up supply
    sysctl net.ipv4.ip_forward                          # must be 0: the Pi does not route

## 2. The gateway

On the Pi, from a checkout of this repository:

    sudo install -d /usr/local/lib/supplyctl
    sudo install -m 644 extras/powercycle/spd3303x.py /usr/local/lib/supplyctl/
    sudo install -m 755 extras/powercycle/supplyctl.py /usr/local/lib/supplyctl/
    python3 /usr/local/lib/supplyctl/spd3303x.py 10.33.0.2 1 --status      # the link works

`/etc/supplyctl.json`, owned by root, with the ceilings a little above the setpoints in use (a
channel without ceilings cannot be switched on):

    {"host": "10.33.0.2",
     "max_volt": {"1": 10.5, "2": 10.0},
     "max_curr": {"1": 0.15, "2": 0.20}}

A user of its own, which can do nothing but run the gateway. It needs a real shell, because sshd
starts the forced command through it; `restrict` takes away everything else (terminal, forwarding,
agent, X11):

    sudo useradd --create-home --shell /bin/sh supply
    sudo install -d -m 700 -o supply -g supply /home/supply/.ssh

## 3. The key

On the Mac, a key for this purpose only:

    ssh-keygen -t ed25519 -f ~/.ssh/supplyctl -N "" -C supplyctl

Its public part goes into `/home/supply/.ssh/authorized_keys` on the Pi (mode 600, owner
`supply`), as one line, preceded by the forced command:

    command="/usr/local/lib/supplyctl/supplyctl.py",restrict ssh-ed25519 AAAA... supplyctl

And in `~/.ssh/config` on the Mac:

    Host supplyctl
        HostName raspi.local
        User supply
        IdentityFile ~/.ssh/supplyctl
        IdentitiesOnly yes

## 4. Checks

    ssh supplyctl status 1               # the status line
    ssh supplyctl volt 1 30              # refused: ..., exit status 2
    ssh supplyctl                        # refused (no request), no shell
    ssh -t supplyctl bash                # refused, no shell
    ping -c 2 10.33.0.2                  # from the Mac: no answer
    journalctl -t supplyctl              # on the Pi: every request, accepted or refused

## 5. Use

    rune2e.py ... --power-cycle-command "ssh supplyctl cycle 1"

and the same for `runparallel.py` after `--`. The server accepts a power cycle when the command
ends with exit status 0; otherwise it asks for a manual one, as without the option.
