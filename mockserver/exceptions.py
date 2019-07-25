class BaseError(Exception):
    pass

class JsonFileNotFund(BaseError):
    pass
class JsonFormatError(BaseError):
    pass
class DirNotFund(BaseError):
    pass
class DictFormatError(BaseError):
    pass
class ContentFormatError(BaseError):
    pass
class ParseError(BaseError):
    pass
class JsonlReadError(BaseError):
    pass
class FileExists(BaseError):
    pass

