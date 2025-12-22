#!/usr/bin/env bash

# find /dev/input/by-id/ -name "*LiQi*" | xargs readlink -f | xargs sudo chown nejdetckenobi:nejdetckenobi
find /dev/input/by-id/ -name "*USB_Composite_Device*" | xargs readlink -f | xargs sudo chown nejdetckenobi:nejdetckenobi
xinput list | grep "Composite" | grep -Po "id=\d+" | cut -d "=" -f 2 | xargs -I% xinput disable %

sudo systemctl restart hot_macropad.service
