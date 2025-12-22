#!/usr/bin/env bash
DISPLAY=:1


cd /home/nejdetckenobi/Projects/hot_macropad/
source venv/bin/activate
# python cli.py --loglevel DEBUG run --wait -d /dev/input/by-id/usb-SayoDevice_SayoDevice_6x4F_0300E72671263B38-event-kbd -c config.json -p page0
# python cli.py --loglevel DEBUG run --wait -d /dev/input/by-id/usb-1189_USB_Composite_Device_CD70134330383836-if01-event-kbd -c config2.json -p docker
python cli.py --loglevel DEBUG run --wait -d /dev/input/by-id/usb-LiQi_Technology̪_USB_Composite_Device_EB60121120041505-event-kbd -c config2.json -p docker
