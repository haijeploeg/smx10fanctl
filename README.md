[![PyPI](https://img.shields.io/pypi/v/smx10fanctl.svg)](https://pypi.org/project/smx10fanctl)

# smx10fanctl 
Smx10fanctl is a fancontroller for Supermicro boards using IPMI raw commands. I created this project because I wanted a quiet homeserver. Supermicro motherboards expects high RPM fans and expects fans that have at least 600RPM minimal. 

I am using a Noctua NH-U12DXi4 CPU cooler which has a minimal RPM of 300. When the CPU is around 20-40 degrees Celcius it will start to ramp up the fans because the Supermicro motherboards have threshholds set. This means that the motherboard wants that the fans are running at least a certain configured RPM speed (you can check those thresholds in your IPMI interface). You can lower the thresholds to 0 for example, but Supermicro motherboards are sometimes reading 0 RPM, I can't find an explaination why Supermicro reads 0RPM, but the internet is full of problems with Noctua fans and Supermicro motherboards. 

Because the motherboard reads 0RPM, it will start to ramp up the fans again, this goes over and over again, which is really annoying. Therefor I created this CLI tool to control the fan speeds on the OS based on the CPU temperature. This script will only work on Linux distributions.

## Tested on
I have developed this cli tool with the following hardware/software.
- Supermicro X10SRH-CF
- Intel Xeon 2680 V4
- Proxmox 6.3.1

The cli tool may or may not work on x8/x9/x11 motherboards as well. Feel free to report back to me if you have tried this.

## Installation

```bash
$ apt install lm-sensors
$ pip install smx10fanctl
```

### Systemd
To run the auto command in systemd, so you can enable the service on the background and let it control your fan speed at startup. You can run the following command.

```bash
### Copy the systemd unit file
$ wget https://raw.githubusercontent.com/haijeploeg/smx10fanctl/main/smx10fanctl.service

### Check the path to smx10fanctl and adjust it in the service file if needed
$ which smx10fanctl
/usr/local/bin/smx10fanctl
$ vim smx10fanctl

### Move the service file
$ mv smx10fanctl /etc/systemd/system/smx10fanctl.service
$ chown root:root /etc/systemd/system/smx10fanctl.service
$ chmod 644 /etc/systemd/system/smx10fanctl.service

### Enable and start the systemd service
$ systemctl enable --now smx10fanctl
```

## Configuration
To configure the application make sure that one of the following files exists:

```bash
/etc/smx10fanctl/smx10fanctl.yml
~/.config/smx10fanctl/smx10fanctl.yml
~/.smx10fanctl/config/smx10fanctl.yml
~/.smx10fanctl.yml
./.smx10fanctl.yml
```

The application will read those configuration files in that order. So `./.smx10fanctl.yml` will overwrite `/etc/smx10fanctl/smx10fanctl.yml`'. For a full list of options and their description see `.smx10fanctl-example.yml` in this repository.

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```bash
### create a virtualenv for development
$ make virtualenv
$ source env/bin/activate


### run smx10fanctl cli application
$ smx10fanctl --help
```

## FAQ
#### My fans are still ramping up after using this tool, is this normal?
Supermicro boards are taking a threshold into account. You need to lower these thresholds to run the fans on a low RPM, e.g. 300RPM. You can lower those thresholds by using the following command. NOTE: adjust FAN1 with your FAN port.

```bash
$ ipmitool sensor thresh FAN1 lower 50 100 200
```

This will lower the non-recoverable setting to 50 (this will cause the RAMP up), the lower critical value to 100 and the lower non-critical value to 200. In the future you can do this with `smx10fanctl`.