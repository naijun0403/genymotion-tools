# genymotion-tools

## feature
- Installing Arm Translation (Thanks to [@zhouziyang/libndk_translation](https://github.com/zhouziyang/libndk_translation)!)

## support android version
Only supporting android version 12, 13 or 14

## how to use
Install arm translation with android version 14

```sh
$ python3 genymotion.py -a 14 -n
```

## FAQ
### Failed to push: ./libndk_translation/system/lib/libnb.so
The problem occurs because libnb.so is a symlink, and the target it points to doesn't actually exist. However, even without it, the problem doesn't exist in the arm translation.