
# Mimeo (Mimeograph)

**Mimeo** is a command line tool and python library generating custom data based on a template.
It can be used by developers, testers or even business analysts in their daily work.


## Installation

Install Mimeo with pip

```sh
pip install mimeograph
```


## Usage/Examples

### Mimeo Configuration

Prepare Mimeo Configuration first
- for a command line tool: in a JSON file
- for a `Mimeograph` python class: in a `dict`

```json
{
  "_templates_": [
    {
      "count": 30,
      "model": {
        "attributes": {
          "xmlns": "http://data-generator.arch.com/default-namespace",
          "xmlns:pn": "http://data-generator.arch.com/prefixed-namespace"
        },
        "SomeEntity": {
          "ChildNode1": 1,
          "ChildNode2": "value-2",
          "ChildNode3": true
        }
      }
    }
  ]
}
```
_You can find more configuration examples in the `examples` folder._

### Mimeograph

#### Command line tool

```sh
mimeo SomeEntity-config.json
```

#### Python library

```python
from mimeo import Mimeograph
from mimeo.config import MimeoConfig

config = {
    # Your configuration
}
mimeo_config = MimeoConfig(config)
Mimeograph(mimeo_config).produce()
```
***
The Mimeo Configuration above will produce 2 files:

```xml
<!-- mimeo-output/mimeo-output-1.xml-->
<SomeEntity xmlns="http://data-generator.arch.com/default-namespace" xmlns:pn="http://data-generator.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <ChildNode2>value-2</ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```
```xml
<!-- mimeo-output/mimeo-output-2.xml-->
<SomeEntity xmlns="http://data-generator.arch.com/default-namespace" xmlns:pn="http://data-generator.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <ChildNode2>value-2</ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```
***

### Mimeo Utils

Mimeo exposes several functions for data generation that will make it more useful for testing purposes.

**Template**
```json
{
  "count": 2,
  "model": {
    "SomeEntity": {
      "id": "{auto_increment()}",
      "randomstring": "{random_str()}",
      "randomint": "{random_int()}",
    }
  }
}
```

**XML Data**
```xml
<SomeEntity>
    <id>00001</id>
    <randomstring>mCApsYZprayYkmKnYWxe</randomstring>
    <randomint>8</randomint>
</SomeEntity>
```
```xml
<SomeEntity>
    <id>00002</id>
    <randomstring>ceaPUqARUkFukZIPeuqO</randomstring>
    <randomint>99</randomint>
</SomeEntity>
```


## Documentation

### Mimeo Configuration

Mimeo configuration is defined in a JSON file using internal settings and data templates.

| Key                             |  Level   |      Required      | Supported values |    Default     | Description                                                                  |
|:--------------------------------|:--------:|:------------------:|:----------------:|:--------------:|------------------------------------------------------------------------------|
| `output_format`                 |  Config  |        :x:         |      `xml`       |     `xml`      | Defines output data format                                                   |
| `output_details`                |  Config  |        :x:         |      object      |      ---       | Defines output details on how it will be consumed                            |
| `output_details/direction`      |  Config  |        :x:         |  `file`, `raw`   |     `file`     | Defines how output will be consumed                                          |
| `output_details/directory_path` |  Config  |        :x:         |      string      | `mimeo-output` | For `file` direction - defines an output directory                           |
| `output_details/file_name`      |  Config  |        :x:         |      string      | `mimeo-output` | For `file` direction - defines an output file name                           |
| `indent`                        |  Config  |        :x:         |     integer      |     `null`     | Defines indent applied in output data                                        |
| `vars`                          |  Config  |        :x:         |      object      |      ---       | Defines variables to be used in a Mimeo Template (read more in next section) |
| `xml_declaration`               |  Config  |        :x:         |     boolean      |    `false`     | Indicates whether an xml declaration should be added to output data          |
| `_templates_`                   |  Config  | :heavy_check_mark: |      array       |      ---       | Stores templates for data generation                                         |
| `count`                         | Template | :heavy_check_mark: |     integer      |      ---       | Indicates number of copies                                                   |
| `model`                         | Template | :heavy_check_mark: |      object      |      ---       | Defines data template to be copied                                           |
| `attributes`                    |  Model   |        :x:         |      object      |      ---       | Defines attributes applied on the root node (mostly used for namespaces)     |

#### Mimeo Vars

Mimeo allows you to define a list of variables.
You can use them in your Mimeo Config by wrapping them in curly brackets [`{VARIABLE}`].

There are only 2 rules for variable names:
- Variable name can include upper-cased letters \[`A-Z`\], underscore \[`_`\] and digits \{`0-9`\} only
- Variable name must start with a letter

Variable can be defined with:
- any atomic value
- any other variable defined
- any Mimeo Util

Example:
```json
{
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1",
            "CUSTOM_VAR_2": 1,
            "CUSTOM_VAR_3": true,
            "CUSTOM_VAR_4": "{CUSTOM_VAR_2}",
            "CUSTOM_VAR_5": "{auto_increment('{}')}"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "{CUSTOM_VAR_1}",
                        "ChildNode2": "{CUSTOM_VAR_2}",
                        "ChildNode3": "{CUSTOM_VAR_3}",
                        "ChildNode4": "{CUSTOM_VAR_4}",
                        "ChildNode5": "{CUSTOM_VAR_5}",
                        "ChildNode6": "{CUSTOM_VAR_6}",
                        "ChildNode7": "{CUSTOM_VAR_7}"
                    }
                }
            }
        ]
    }
```

### Mimeo CLI

When using Mimeo command line tool you can overwrite Mimeo Configuration properties:

| Short option | Long option       | Description                                            |
|:------------:|:------------------|:-------------------------------------------------------|
|      -x      | --xml-declaration | overwrite the `xml_declaration` property               |
|      -i      | --indent          | overwrite the `indent` property                        |
|      -o      | --output          | overwrite the `output_details/direction` property      |
|      -d      | --directory       | overwrite the `output_details/directory_path` property |
|      -f      | --file            | overwrite the `output_details/file_name` property      |

### Mimeo Utils

You can use several predefined functions to generate data by using them within curly braces:
```xml
<id>{auto_increment()}</id>
```

| Function                                                                   | Example                         | Data                                                                                                  |
|:---------------------------------------------------------------------------|:--------------------------------|:------------------------------------------------------------------------------------------------------|
| `auto_increment()`                                                         |                                 | Generates next integer in context of a model (in nested templates it will use a separated context)    |
| `auto_increment(<STRING_PATTERN>)`                                         | `auto_increment('MYID{:010d}')` | Same as `auto_increment()` but the integer is used in a string pattern provided                       |
| `curr_iter()`                                                              |                                 | Generates a value of the current iteration in a Mimeo Template context                                |
| `curr_iter(<MODEL_NAME>)`                                                  | `curr_iter('SomeEntity')`       | Generates a value of the current iteration in a specific Mimeo Model context                          |
| `key()`                                                                    |                                 | Generates a key unique across all Mimeo Models and being the same within a single Mimeo Model context |
| `get_key(<MODEL_NAME>, <ITERATION>)`                                       | `get_key('SomeEntity')`         | Retrieves a key from a specific context, optionally using position (by default it takes the last)     |
| `random_str()`                                                             |                                 | Generates a random string value of the default length: 20 characters                                  |
| `random_str(<LENGTH>)`                                                     | `random_str(2)`                 | Generates a random string value of the customized length                                              |
| `random_int()`                                                             |                                 | Generates a random integer value within the default range: 0-99                                       |
| `random_int(<LIMIT>)`                                                      | `random_int(10)`                | Generates a random integer value within the custom range: 0-<LIMIT>                                   |
| `date()`                                                                   |                                 | Generates a today's date in format YYYY-MM-DD                                                         |
| `date(<DAYS_DELTA>)`                                                       | `date(-1)`                      | Generates a date with customized days in format YYYY-MM-DD                                            |
| `date_time()`                                                              |                                 | Generates a current date time in format YYYY-MM-DD'T'HH:mm:SS                                         |
| `date_time(<DAYS_DELTA>, <HOURS_DELTA>, <MINUTES_DELTA>, <SECONDS_DELTA>)` | `date(hours=5, minutes=-3)`     | Generates a date time with customized time in format YYYY-MM-DD'T'HH:mm:SS                            |


## License

MIT


## Authors

- [@TomaszAniolowski](https://www.github.com/TomaszAniolowski)

