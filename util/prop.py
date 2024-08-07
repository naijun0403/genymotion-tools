class PropManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.properties = {}
        self._parse_file()

    def _parse_file(self):
        """Parse the build.prop file and load properties."""
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    self.properties[key] = value

    def add_property(self, key, value):
        """Add a new property or update an existing one."""
        self.properties[key] = value

    def update_property(self, key, value):
        """Update an existing property."""
        if key in self.properties:
            self.properties[key] = value
        else:
            print(f'Key "{key}" not found.')

    def delete_property(self, key):
        """Delete an existing property."""
        if key in self.properties:
            del self.properties[key]
        else:
            print(f'Key "{key}" not found.')

    def save(self):
        """Save properties back to the build.prop file."""
        with open(self.file_path, 'w') as file:
            for key, value in self.properties.items():
                file.write(f'{key}={value}\n')