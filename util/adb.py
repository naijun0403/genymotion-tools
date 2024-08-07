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

    def push(self, local_path, remote_path, as_root=False):
        """Push a file from the local machine to the connected device."""
        if not os.path.exists(local_path):
            print(f"Local path does not exist: {local_path}")
            return False

        local_path_quoted = f"'{local_path}'"
        remote_path_quoted = f"'{remote_path}'"

        full_command = f"{self.adb_path} push {local_path_quoted} {remote_path_quoted}"
        result = self._run_command(full_command, use_shell=True)

        if result is None:
            return False

        if as_root:
            self.shell(f"chown root:root {remote_path_quoted}", as_root=True)
            self.shell(f"chmod 644 {remote_path_quoted}", as_root=True)

        return True

    def pull(self, remote_path, local_path, as_root=False):
        """Pull a file from the connected device to the local machine."""
        if as_root and not self.is_root:
            if not self.root():
                print("Command requires root, but root access couldn't be obtained")
                return False

        remote_path_quoted = f"'{remote_path}'"
        local_path_quoted = f"'{local_path}'"

        full_command = f"{self.adb_path} pull {remote_path_quoted} {local_path_quoted}"
        result = self._run_command(full_command, use_shell=True)
        return result is not None

    def merge_pull(self, remote_path, local_base_path, as_root=False):
        """
        Recursively pull files and directories, merging with existing content on the local machine.
        """
        if as_root and not self.is_root:
            if not self.root():
                print("Command requires root, but root access couldn't be obtained")
                return False

        if self.shell(f"[ -e {remote_path} ] && echo 'exists' || echo 'not exists'", as_root=as_root) != "exists":
            print(f"Remote path does not exist: {remote_path}")
            return False

        if self.shell(f"[ -f {remote_path} ] && echo 'file' || echo 'not file'", as_root=as_root) == "file":
            return self.pull(remote_path, os.path.join(local_base_path, os.path.basename(remote_path)), as_root=as_root)

        remote_files = self.shell(f"find {remote_path} -type f", as_root=as_root).split('\n')
        
        for remote_file in remote_files:
            if not remote_file:
                continue
            relative_path = os.path.relpath(remote_file, remote_path)
            local_file_path = os.path.join(local_base_path, relative_path)
            
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            
            if not self.pull(remote_file, local_file_path, as_root=as_root):
                print(f"Failed to pull: {remote_file}")
                return False

        return True

    def merge_push(self, local_path, remote_base_path, as_root=False):
        """
        Recursively push files and directories, merging with existing content on the device.
        """
        if not os.path.exists(local_path):
            print(f"Local path does not exist: {local_path}")
            return False

        if os.path.isfile(local_path):
            return self.push(local_path, os.path.join(remote_base_path, os.path.basename(local_path)), as_root=as_root)

        for root, dirs, files in os.walk(local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, local_path)
                if relative_path == ".":
                    remote_file_path = os.path.join(remote_base_path, file)
                else:
                    remote_file_path = os.path.join(remote_base_path, relative_path, file)
                
                remote_dir = os.path.dirname(remote_file_path)
                self.shell(f"mkdir -p {remote_dir}", as_root=as_root)
                
                if not self.push(local_file_path, remote_file_path, as_root=as_root):
                    print(f"Failed to push: {local_file_path}")
                    return False

        return True

    def devices(self):
        """List connected devices."""
        return self._run_command(f"{self.adb_path} devices", use_shell=True)

    def is_device_connected(self):
        """Check if a device is connected."""
        devices = self.devices()
        return devices is not None and len(devices.split('\n')) > 1