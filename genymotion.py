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
        default='14',
        choices=['12', '13', '14']
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
    
    print('[!] All Process is finish!')


if __name__ == "__main__":
    main()