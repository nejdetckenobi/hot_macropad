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

This is the place you should be looking to configure your device's behaviours.
We have adapters that allows you to control various things.
You can use them or write your own adapter.

## Using an adapter

Replace the value for the desired key code in your action pages like below.

```json
{
  "adapter": XXX,
  "parameter1": YYY,
  "parameter2": ZZZ,
  ...
}
```

After that, run the cli in the `run` mode.


## Default Adapters

Here are the list of the adapters available to use.

| `adapter` value (XXX) | parameters (XXX, YYY, ...) | Note |
|-----------------|------------|------|
| `actionpagechangers.NextActionPage` | - | It sets your action page to the next one. If you're at the last page, you'll be taken to the first one. |
| `actionpagechangers.PreviousActionPage` | - | It sets your action page to the previous one. If you're at the first page, you'll be taken to the last one. |
| `actionpagechangers.ActionPageSetter` | `page_number`: The action page you want to set | It sets your layout to the layout specified with `page_number`. If your configuration file does not have enough pages, nothing will happen. |
| `commandrunners.GlobalCommandRunner` | `command`: The string you want to use | This is a copy-paste adapter. It pastes the string provided with `command` parameter and hits `Enter`. |
| `commandrunners.CommandPasteAndReturn` | `command`: The command you want to run when you release the key | Runs the command specified as `command`. Provides no output. |
| `padlocker.PadLocker` | `deltaseconds`: The time you should hold in seconds to invoke something | Locks/Unlocks the device when you press and hold the button for `deltaseconds`. |

## Writing your own Adapter

We have base classes for each key event: Press, Hold, Relase.

| Base action class | Description |
|-------------------|-------------|
| `base.BaseAction` | You probably don't need this |
| `base.PressExecuteAction` | Triggers when you press the key |
| `base.ReleaseExecuteAction` | Triggers when you release the pressed key |
| `base.HoldExecuteAction` | Triggers when you press and hold the key. It is triggered once per hold. |

Let's create an adapter that prints `Hello, YOUR_NAME` when you release a key

```python
# adapters/myadapter.py
from adapters.base import ReleaseExecuteAction


class MyPrettyAdapter(ReleaseExecuteAction):
    def __init__(self, name):  # Since we need a name to pass to the adapter
        super(MyPrettyAdapter, self).__init__()
        self.name = name
    
    def run(self, context=None):  # You should override this method. Context is the state of macropad
        print("Hello,", self.name)
        super(MyPrettyAdapter, self).run(context=context)  # Do not forget this line.

    def __repr__(self):  # Override this record to see the log in the cli output.
        return "{}(\"{}\")".format(self.__class__.__name__, self.name)
```

Then we should go to the configuration to assign our adapter to the key we want

```json
// configuration_v2.json

[
  {
    "KEY_L": {  // We want to use this key in our first action page
      "adapter": "adapters.myadapter",
      "name": "MAHMUT"  // "MAHMUT" is a known male name
    },
    "KEY_K": {  // We also want this key in our first action page
      "adapter": "adapters.myadapter",
      "name": "HAYDAR"  // "HAYDAR" is also a known male name
    }
  },
  {
    "KEY_0": {  // We want to use this key in our second action page
      "adapter": "adapters.myadapter",
      "name": "NEJDET"
    }
  }
]
```

Then run the cli tool in `run` mode. You're ready to go!