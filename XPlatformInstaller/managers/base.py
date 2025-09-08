class PackageManager:
    def search_package(self, name):
        raise NotImplementedError

    def validate_package(self, name):
        raise NotImplementedError

    def clean_package_list(self, package_list):
        raise NotImplementedError

    def generate_install_command(self, package_list):
        raise NotImplementedError
