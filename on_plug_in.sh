#!/usr/bin/env sh

export XAUTHORITY="/run/user/1001/gdm/Xauthority"
export DISPLAY=":1"

xinput list | grep "SayoDevice" | cut -f 2 | cut -d "=" -f 2 | xargs -I% xinput disable %
