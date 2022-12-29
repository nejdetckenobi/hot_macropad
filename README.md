# hot_macropad: A project that allows you to make any keyboard a macropad

This project is for making macro pads from keyboards or keyboard-like devices.

No install script at the moment. Just clone the project.


## How to configure

- First of all, you need to disable the input read for the device.
  You can use `xinput` for that. 
  Run `xinput list` first.
  You should get an output similar to that.
  ```
  ⎡ Virtual core pointer                    	id=2	[master pointer  (3)]
  ⎜   ↳ Virtual core XTEST pointer              	id=4	[slave  pointer  (2)]
  ⎜   ↳ USB OPTICAL MOUSE                       	id=11	[slave  pointer  (2)]
  ⎜   ↳ SayoDevice SayoDevice 6x4F Keyboard     	id=12	[slave  pointer  (2)]
  ⎜   ↳ SayoDevice SayoDevice 6x4F Mouse        	id=17	[slave  pointer  (2)]
  ⎣ Virtual core keyboard                   	id=3	[master keyboard (2)]
      ↳ Virtual core XTEST keyboard             	id=5	[slave  keyboard (3)]
      ↳ Power Button                            	id=6	[slave  keyboard (3)]
      ↳ Video Bus                               	id=7	[slave  keyboard (3)]
      ↳ Sleep Button                            	id=8	[slave  keyboard (3)]
      ↳ Video Bus                               	id=9	[slave  keyboard (3)]
      ↳ Power Button                            	id=10	[slave  keyboard (3)]
      ↳ HD WebCam: HD WebCam                    	id=15	[slave  keyboard (3)]
      ↳ AT Translated Set 2 keyboard            	id=16	[slave  keyboard (3)]
      ↳ SayoDevice SayoDevice 6x4F Keyboard     	id=13	[slave  keyboard (3)]
      ↳ SayoDevice SayoDevice 6x4F              	id=14	[slave  keyboard (3)]
  ``` 

  In this output, since my device has multiple inputs and since all `id` numbers change when you remove and plug in again, I used the command below to disable all inputs for SayoDevice interfaces
  ```bash
  xinput list | grep "SayoDevice" | cut -f 2 | cut -d "=" -f 2 | xargs -I% xinput disable %
  ```
  **Do not copy the command, build a command that satisfies your needs.**
  After this point, if you try pressing buttons of your device you should notice that it will not work.

- Run the command below to see your input devices and remember the name of the device file that represents your device. 
  ```bash
  ls -1 /dev/input/by-id/
  ```
  You may want to run this command several times and remove/plug in your device to see which interface is created for your device.
- Run the command below to see your device's keypresses. 
  Press and release every single button on your device. 
  Take notes based on the output.
  This will allow you to recognize the key codes in the configuration file.
  Press `Ctrl + C` to stop.

- Run the command below and after that, press and release every single button on your device.
  ```bash
  python cli.py configure -d DEVICE_FILE_FROM_PREVIOUS_STEP -o configuration.json
  ```
  
  When you're done, release all buttons, then press `Ctrl + C`.
  You should notice a `configuration.json` file created in the project directory.
  Open that file with your favorite text editor.
  You'll see a list (`[]`) that contains an object (`{}`) with bunch of key codes in it.
  You should notice that you already saw these key codes in the previous step.
  You should see `null` right next to every key code.

- Change the `null` values according to the [configuration section](#configuration-options)
  

# Configuration Options

