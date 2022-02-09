class PyperclipBackup:
    @staticmethod
    def copy(_):
        print(
            "Can't copy to clipboard, pyperclip is not installed. Run "
            "pip install pyperclip"
        )
