from util.download import download_file
from util.md5 import calculate_md5
from util.tar import extract_tar
from util.adb import ADB
from util.prop import PropManager

class Ndk:
    def __init__(self, android_ver: str) -> None:
        self.dl_links = {
            '12': ['https://github.com/zhouziyang/libndk_translation/raw/master/libndk_translation-12.0.0.tar', 'e99a8ea60509509cd2353e0ac0b61862'],
            '13': ['https://github.com/zhouziyang/libndk_translation/raw/master/libndk_translation-12.0.0.tar', 'e99a8ea60509509cd2353e0ac0b61862'],
            '14': ['https://github.com/zhouziyang/libndk_translation/raw/master/libndk_translation-12.0.0.tar', 'e99a8ea60509509cd2353e0ac0b61862']
        }
        self.android_ver = android_ver

    def download(self) -> None:
        print('[*] Attampts to download NDK tools')

        download_file(self.dl_links[self.android_ver][0], 'libndk_translation.tar')

        print('[*] verify checksum...')

        downloaded_checksum = calculate_md5('libndk_translation.tar')

        if downloaded_checksum != self.dl_links[self.android_ver][1]:
            print('[!] Unmatch checksum! attampts to redownload')
            return self.download()
        
        print('[*] Successfully download ndk tools')

        print('[*] extracts files...')

        extract_tar('libndk_translation.tar', './libndk_translation/')

    def patch(self) -> None:
        print('[*] patching files')

        adb = ADB()

        connected = adb.is_device_connected()

        if not connected:
            print('[!] Sorry, your emulator is not connected')
            return
        
        print('[*] merge system for arm translation')

        adb.root()

        adb.shell('mount -o rw,remount /')

        adb.merge_push('./libndk_translation/system', '/system', as_root=True)
        
        print('[*] modify system props')
        
        adb.pull('/system/build.prop', './libndk_translation/', as_root=True)

        prop = PropManager('./libndk_translation/build.prop')
        prop.add_property('ro.product.cpu.abilist', 'x86_64,x86,arm64-v8a,armeabi-v7a,armeabi')
        prop.add_property('ro.product.cpu.abilist32', 'x86,armeabi-v7a,armeabi')
        prop.add_property('ro.product.cpu.abilist64', 'x86_64,arm64-v8a')
        prop.update_property('ro.system.product.cpu.abilist', f'{prop.properties['ro.system.product.cpu.abilist']},arm64-v8a,armeabi-v7a,armeabi')
        prop.update_property('ro.system.product.cpu.abilist32', f'{prop.properties['ro.system.product.cpu.abilist32']},armeabi-v7a,armeabi')
        prop.update_property('ro.system.product.cpu.abilist64', f'{prop.properties['ro.system.product.cpu.abilist64']},arm64-v8a')
        prop.update_property('ro.dalvik.vm.native.bridge', 'libndk_translation.so')
        prop.add_property('ro.berberis.version', '0.2.3')
        prop.add_property('ro.dalvik.vm.isa.arm64', 'x86_64')
        prop.add_property('ro.dalvik.vm.isa.arm', 'x86')
        prop.add_property('ro.enable.native.bridge.exec', '1')
        prop.add_property('ro.enable.native.bridge.exec64', '1')
        prop.add_property('ro.ndk_translation.version', '0.2.3')

        prop.add_property('ro.odm.product.cpu.abilist', 'x86_64,x86,arm64-v8a,armeabi-v7a,armeabi')
        prop.add_property('ro.odm.product.cpu.abilist32', 'x86,armeabi-v7a,armeabi')
        prop.add_property('ro.odm.product.cpu.abilist64', 'x86_64,arm64-v8a')

        prop.save()

        adb.push('./libndk_translation/build.prop', '/system/build.prop', as_root=True)

        adb.pull('/system/vendor/build.prop', './libndk_translation/vendor.build.prop', as_root=True)
        
        vendor_prop = PropManager('./libndk_translation/vendor.build.prop')
        vendor_prop.update_property('ro.vendor.product.cpu.abilist', f'{vendor_prop.properties['ro.vendor.product.cpu.abilist']},arm64-v8a,armeabi-v7a,armeabi')
        vendor_prop.update_property('ro.vendor.product.cpu.abilist32', f'{vendor_prop.properties['ro.vendor.product.cpu.abilist32']},armeabi-v7a,armeabi')
        vendor_prop.update_property('ro.vendor.product.cpu.abilist64', f'{vendor_prop.properties['ro.vendor.product.cpu.abilist64']},arm64-v8a')

        vendor_prop.save()

        adb.push('./libndk_translation/vendor.build.prop', '/system/vendor/build.prop', as_root=True)

        adb.shell('mount -o ro,remount /')

        print('[!] Successfully patched for arm translation!, please restart your genymotion!')