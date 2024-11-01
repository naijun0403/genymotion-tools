import os
import subprocess
import time

class ADB:
    def __init__(self, adb_path="adb"):
        self.adb_path = adb_path
        self.is_root = False

    def _run_command(self, command: str, use_shell: bool = False):
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=use_shell
            )
            output, error = process.communicate()
            if process.returncode != 0:
                print(f"Error executing command: {error.strip()}")
                return None
            return output.strip()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def root(self):
        """Enable root access for ADB."""
        result = self._run_command(f"{self.adb_path} root", use_shell=True)
        if result is not None and "cannot run as root" not in result.lower():
            self.is_root = True
            time.sleep(2)
            print("ADB is now running as root")
            return True
        else:
            print("Failed to gain root access")
            return False

    def shell(self, command, as_root=False):
        """Execute a shell command on the connected device."""
        if as_root and not self.is_root:
            if not self.root():
                print("Command requires root, but root access couldn't be obtained")
                return None

        if as_root:
            full_command = f"{self.adb_path} shell 'su -c \"{command}\"'"
        else:
            full_command = f"{self.adb_path} shell {command}"
        
        return self._run_command(full_command, use_shell=True)

    def push(self, local_path, remote_path):
        """Push a file or directory from the local machine to the connected device."""
        if not os.path.exists(local_path):
            print(f"Local path does not exist: {local_path}")
            return False

        full_command = f"{self.adb_path} push '{local_path}' '{remote_path}'"
        print(full_command)
        result = self._run_command(full_command, use_shell=True)

        if result is None:
            return False

        return True

    def pull(self, remote_path, local_path, as_root=False):
        """Pull a file or directory from the connected device to the local machine."""
        if as_root and not self.is_root:
            if not self.root():
                print("Command requires root, but root access couldn't be obtained")
                return False

        full_command = f"{self.adb_path} pull '{remote_path}' '{local_path}'"
        result = self._run_command(full_command, use_shell=True)
        return result is not None

    def devices(self):
        """List connected devices."""
        return self._run_command(f"{self.adb_path} devices", use_shell=True)

    def is_device_connected(self):
        """Check if a device is connected."""
        devices = self.devices()
        return devices is not None and len(devices.split('\n')) > 1