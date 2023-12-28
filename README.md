# Cross-Platform Gigabyte Monitor Configuration In Python

## Introduction

A script to configure Gigabyte monitor attributes (brightness, contrast, kvm switch, etc...) without bloatware.

## Usage
```text
usage: monitor.py [-h] -p
                  {brightness,contrast,sharpness,low-blue-light,kvm-switch,colour-mode,rgb-red,rgb-green,rgb-blue}
                  -v [0-255]
```

## Dependencies
* [pyhidapi](https://github.com/apmorton/pyhidapi) (Make sure to install the hidapi shared library)

## Caveats
- Was only tested under Windows 11, with a M27U monitor.
- The supplied script supports only writing attributes and not reading them.
- Only works from the currently active KVM input device.

## Credits
The script is based on the following works:
- @kelvie at https://github.com/kelvie/gbmonctl
- @P403n1x87 at https://github.com/P403n1x87/m27q
- @MarekPrzydanek at https://github.com/MarekPrzydanek/GigabyteMonitorController