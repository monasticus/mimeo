import json
import logging
from os import path, walk

from mimeo import MimeoConfig, Mimeograph
from mimeo.cli import MimeoArgumentParser
from mimeo.cli.exc import EnvironmentNotFound, EnvironmentsFileNotFound

logger = logging.getLogger(__name__)


class MimeoJob:

    DEFAULT_ENVS_FILE_PATH = "mimeo.envs.json"

    def __init__(self):
        self.args = MimeoArgumentParser().parse_args()

    def run(self):
        self._customize_logging_level()

        logger.info("Starting a Mimeo job")
        for config_path in self._get_paths():
            logger.info(f"Data generation from Mimeo Config: {config_path}")
            mimeo_config = self._get_config(config_path)
            Mimeograph(mimeo_config).process()

    def _customize_logging_level(self):
        if self.args.silent:
            logging.getLogger("mimeo").setLevel(logging.WARNING)
        elif self.args.debug:
            logging.getLogger("mimeo").setLevel(logging.DEBUG)
        elif self.args.fine and hasattr(logging, "FINE"):
            logging.getLogger("mimeo").setLevel(logging.FINE)

    def _get_paths(self) -> list:
        file_paths = []
        for file_path in self.args.paths:
            if path.isdir(file_path):
                for dir_path, _, file_names in walk(file_path):
                    for file_name in file_names:
                        file_paths.append(f"{dir_path}/{file_name}")
            elif path.isfile(file_path):
                file_paths.append(file_path)
        return file_paths

    def _get_config(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
            if self.args.http_env is not None:
                envs_file = self.args.http_envs_file if self.args.http_envs_file is not None else self.DEFAULT_ENVS_FILE_PATH
                self._customize_output_details_with_env(config, envs_file, self.args.http_env)
            if self.args.xml_declaration is not None:
                xml_declaration = self.args.xml_declaration.lower() == "true"
                logger.fine(f"Overwriting xml_declaration to [{xml_declaration}]")
                config[MimeoConfig.XML_DECLARATION_KEY] = xml_declaration
            if self.args.indent is not None:
                logger.fine(f"Overwriting indent to [{self.args.indent}]")
                config[MimeoConfig.INDENT_KEY] = self.args.indent
            if self.args.output is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY, self.args.output)
            if self.args.directory is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_DIRECTORY_PATH_KEY, self.args.directory)
            if self.args.file is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_FILE_NAME_KEY, self.args.file)
            if self.args.http_method is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_METHOD_KEY, self.args.http_method)
            if self.args.http_protocol is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_PROTOCOL_KEY, self.args.http_protocol)
            if self.args.http_auth is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_AUTH_KEY, self.args.http_auth)
            if self.args.http_host is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_HOST_KEY, self.args.http_host)
            if self.args.http_port is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_PORT_KEY, self.args.http_port)
            if self.args.http_endpoint is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_ENDPOINT_KEY, self.args.http_endpoint)
            if self.args.http_user is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_USERNAME_KEY, self.args.http_user)
            if self.args.http_password is not None:
                self._customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_PASSWORD_KEY, self.args.http_password)
        mimeo_config = MimeoConfig(config)
        logger.debug(f"Mimeo Config: {mimeo_config}")
        return mimeo_config

    @classmethod
    def _customize_output_details_with_env(cls, config, envs_path, env_name):
        if path.exists(envs_path):
            with open(envs_path) as envs_file:
                envs = json.load(envs_file)
                if env_name in envs:
                    env = envs[env_name]
                    logger.debug(f"Using environment [{env_name}] from file [{envs_path}]: [{env}]")
                    for prop in [MimeoConfig.OUTPUT_DETAILS_PROTOCOL_KEY,
                                 MimeoConfig.OUTPUT_DETAILS_HOST_KEY,
                                 MimeoConfig.OUTPUT_DETAILS_PORT_KEY,
                                 MimeoConfig.OUTPUT_DETAILS_AUTH_KEY,
                                 MimeoConfig.OUTPUT_DETAILS_USERNAME_KEY,
                                 MimeoConfig.OUTPUT_DETAILS_PASSWORD_KEY]:
                        prop_value = env.get(prop)
                        if prop_value is not None:
                            cls._customize_output_details(config, prop, prop_value)
                else:
                    raise EnvironmentNotFound(env_name, envs_path)
        else:
            raise EnvironmentsFileNotFound(envs_path)

    @classmethod
    def _customize_output_details(cls, config, key, value):
        if config.get(MimeoConfig.OUTPUT_DETAILS_KEY) is None:
            config[MimeoConfig.OUTPUT_DETAILS_KEY] = {}

        logger.fine(f"Overwriting output details' {key} to [{value}]")
        config[MimeoConfig.OUTPUT_DETAILS_KEY][key] = value
