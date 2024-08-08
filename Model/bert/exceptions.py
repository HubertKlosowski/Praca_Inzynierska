class ParameterValueException(Exception):
    def __init__(self, message="Value given to parameter is invalid"):
        self.message = message
        super().__init__(self.message)


class DataframeException(Exception):
    def __init__(self, message="Dataframe is invalid"):
        self.message = message
        super().__init__(self.message)
