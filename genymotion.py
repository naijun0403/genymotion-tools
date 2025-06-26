#!/usr/bin/env python3

import argparse
import platform
from stuff.ndk import Ndk

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-a',
        '--android-version',
        dest='android',
        help='Specific android version',
        default='15',
        choices=['12', '13', '14', '15']
    )

    parser.add_argument(
        '-n',
        '--install-ndk-translation',
        dest='ndk',
        help='Install Arm Translation (libndk_translation)',
        action='store_true'
    )

    args = parser.parse_args()

    if args.ndk:
        arch = platform.machine()

        if arch == 'i686' or arch == 'x86_64':
            ndk = Ndk(android_ver=args.android)
            ndk.download()
            ndk.patch()
        else:
            print(f'[!] Sorry, {arch} architecture is not supported. Only x86 and x86_64 are supported for now.')
            return
    
    print('[!] All Process is finish!')


if __name__ == "__main__":
    main()