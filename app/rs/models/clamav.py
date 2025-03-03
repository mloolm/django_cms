import pyclamd

class ClamAVScanner:
    def __init__(self, host='clam', port=3310, shared_dir='/shared'):
        self.host = host
        self.port = port
        self.shared_dir = shared_dir
        self.clamd = None

    def connect_to_clamav(self):
        if self.clamd:
            return
        try:
            # Create a connection to ClamAV
            self.clamd = pyclamd.ClamdNetworkSocket(self.host, self.port)
            self.clamd.ping()  # Проверка подключения
            print(f"Connected to ClamAV at {self.host}:{self.port}")
        except pyclamd.ConnectionError as e:
            print(f"Failed to connect to ClamAV: {e}")

    def scan_file(self, file_path):
        self.connect_to_clamav()

        if self.clamd:
            try:
                # Scanning file
                result = self.clamd.scan_file(file_path)

                if result:
                    return result
                else:
                    return 0

            except Exception as e:
                return f"Error scanning file {file_path}: {e}"
        else:
            return "Not connected to ClamAV"
