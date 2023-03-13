import pytest

from mimeo.config.mimeo_config import MimeoOutputDetails
from mimeo.exceptions import UnsupportedOutputDirection


def test_parsing_output_details_stdout():
    output_details = {
      "direction": "stdout"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "stdout"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None


def test_parsing_output_details_stdout_with_file_customization():
    output_details = {
      "direction": "stdout",
      "directory_path": "out",
      "file_name": "out-file"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "stdout"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None


def test_parsing_output_details_file_default():
    output_details = {
        "direction": "file"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "file"
    assert mimeo_output_details.directory_path == "mimeo-output"
    assert mimeo_output_details.file_name_tmplt == "mimeo-output-{}.xml"


def test_parsing_output_details_file_customized():
    output_details = {
        "direction": "file",
        "directory_path": "out",
        "file_name": "out-file"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "file"
    assert mimeo_output_details.directory_path == "out"
    assert mimeo_output_details.file_name_tmplt == "out-file-{}.xml"


def test_parsing_output_details_unsupported_direction():
    output_details = {
        "direction": "unsupported_direction"
    }

    with pytest.raises(UnsupportedOutputDirection) as err:
        MimeoOutputDetails("xml", output_details)

    assert err.value.args[0] == "Provided direction [unsupported_direction] is not supported!"
