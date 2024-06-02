from csv import DictReader


class PromptFileFormatError(Exception):
    def __init__(self, file_path: str):
        message = f"File \'{file_path}\' is not formatted properly.\nShould begin: \'key,text\'"
        super().__init__(message)


class Prompt:
    def __init__(self, key: str, text: str):
        self.__key = key
        self.__text = text

    @property
    def key(self) -> str:
        return self.__key

    @property
    def text(self) -> str:
        return self.__text

    def set_text(self, new_text: str) -> None:
        self.__text = new_text
        return None

    def __str__(self) -> str:
        return self.text


class PromptManager:
    def __init__(self, file_path: str="prompts.csv"):
        assert len(file_path) > 4 and file_path[-4:] == ".csv", FileNotFoundError(file_path)
        self.__file_path = file_path
        self.__prompts_data = {}
        with open(file_path, 'r') as file:
            reader = DictReader(file)
            for row in reader:
                key = row["key"]
                if key in self.__prompts_data:
                    raise PromptFileFormatError(file_path)
                self.__prompts_data[key] = row["text"]

    @property
    def file_path(self) -> str:
        return self.__file_path

    def __getitem__(self, key: str) -> Prompt:
        return Prompt(key, self.__prompts_data[key])

    def get(self, key: str) -> Prompt:
        return self.__getitem__(key)
