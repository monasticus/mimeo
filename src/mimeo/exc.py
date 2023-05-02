"""The Mimeo CLI Exceptions module.

It contains all custom exceptions related to Mimeo CLI:
    * EnvironmentNotFound
        A custom Exception class for not found environment.
    * EnvironmentsFileNotFound
        A custom Exception class for not found environments file.
"""


class EnvironmentNotFound(Exception):
    """A custom Exception class for not found environment.

    Raised while attempting to access an environment that does not
    exist.
    """

    def __init__(self, env_name: str, envs_file_path: str):
        """Initialize EnvironmentNotFound exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        env_name : str
            An environment name
        envs_file_path : str
            An environments file path
        """
        super().__init__(f"No such env [{env_name}] in environments file [{envs_file_path}]")


class EnvironmentsFileNotFound(Exception):
    """A custom Exception class for not found environments file.

    Raised while attempting to access an environments file that does
    not exist.
    """

    def __init__(self, envs_file_path: str):
        """Initialize EnvironmentsFileNotFound exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        envs_file_path : str
            An environments file path
        """
        super().__init__(f"Environments file not found [{envs_file_path}]")
