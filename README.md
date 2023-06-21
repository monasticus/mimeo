# Mimeo (Mimeograph)

[![License](https://img.shields.io/github/license/TomaszAniolowski/mimeo?label=License&style=plastic)](https://github.com/TomaszAniolowski/mimeo/blob/develop/LICENSE)
[![Version](https://img.shields.io/pypi/v/mimeograph?color=blue&label=PyPI&style=plastic)](https://pypi.org/project/mimeograph/)
[![Python](https://img.shields.io/pypi/pyversions/mimeograph?label=Python&style=plastic)](https://www.python.org/)  
[![Build](https://img.shields.io/github/actions/workflow/status/TomaszAniolowski/mimeo/test.yml?color=brightgreen&label=Test%20Mimeo&style=plastic)](https://github.com/TomaszAniolowski/mimeo/actions/workflows/test.yml?query=branch%3Amain)
[![Code Coverage](https://img.shields.io/badge/Code%20Coverage-100%25-brightgreen?style=plastic)](https://github.com/TomaszAniolowski/mimeo/actions/workflows/coverage_badge.yml?query=branch%3Amain)

[Mimeo](https://github.com/TomaszAniolowski/mimeo) is a command line tool and python library generating NoSQL data based on a template.
It can be used by developers, testers or even business analysts in their daily work.


## Installation

Install Mimeo with pip

```sh
pip install mimeograph
```


## Usage/Examples

### Mimeo Configuration

Prepare Mimeo Configuration first

<table>
    <tr>
        <th></th>
        <th>JSON</th>
        <th>XML</th>
    </tr>
    <tr>
        <td><b>CLI</b></td>
        <td valign="top">SomeEntity-config.json

```json
{
  "_templates_": [
    {
      "count": 30,
      "model": {
        "SomeEntity": {
          "@xmlns": "http://mimeo.arch.com/default-namespace",
          "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
          "ChildNode1": 1,
          "ChildNode2": "value-2",
          "ChildNode3": true
        }
      }
    }
  ]
}
```
</td>
    <td valign="top">SomeEntity-config.xml

```xml
<mimeo_configuration>
    <_templates_>
        <_template_>
            <count>30</count>
            <model>

                <SomeEntity
                    xmlns="http://mimeo.arch.com/default-namespace"
                    xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
                    <ChildNode1>1</ChildNode1>
                    <pn:ChildNode2>value-2</pn:ChildNode2>
                    <ChildNode3>true</ChildNode3>
                </SomeEntity>

            </model>
        </_template_>
    </_templates_>
</mimeo_configuration>
```
</td>
  </tr>
    <tr>
        <td rowspan="2"><b>Python</b></td>
        <td valign="top">

```python
from mimeo import MimeoConfigFactory

config = {
  "_templates_": [
    {
      "count": 30,
      "model": {
        "SomeEntity": {
          "@xmlns": "http://mimeo.arch.com/default-namespace",
          "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
          "ChildNode1": 1,
          "ChildNode2": "value-2",
          "ChildNode3": True
        }
      }
    }
  ]
}
mimeo_config = MimeoConfigFactory.parse(config)
```
</td>
    <td valign="top">

```python
from mimeo import MimeoConfigFactory

config = (
    '<mimeo_configuration>'
    '    <_templates_>'
    '        <_template_>'
    '            <count>30</count>'
    '            <model>'
    ''
    '                <SomeEntity'
    '                    xmlns="http://mimeo.arch.com/default-namespace"'
    '                    xmlns:pn="http://mimeo.arch.com/prefixed-namespace">'
    '                    <ChildNode1>1</ChildNode1>'
    '                    <pn:ChildNode2>value-2</pn:ChildNode2>'
    '                    <ChildNode3>true</ChildNode3>'
    '                </SomeEntity>'
    ''
    '            </model>'
    '        </_template_>'
    '    </_templates_>'
    '</mimeo_configuration>')
mimeo_config = MimeoConfigFactory.parse(config)
```
</td>
  </tr>
    <tr>
        <td valign="top">

```python
from mimeo import MimeoConfigFactory

config = "SomeEntity-config.json"
mimeo_config = MimeoConfigFactory.parse(config)
```
</td>
    <td valign="top">

```python
from mimeo import MimeoConfigFactory

config = "SomeEntity-config.xml"
mimeo_config = MimeoConfigFactory.parse(config)
```
</td>
  </tr>
</table>


_You can find more configuration examples in the `examples` folder._

### Data generation

The Mimeo Configuration above will produce 2 files:

```xml
<!-- mimeo-output/mimeo-output-1.xml-->
<SomeEntity xmlns="http://mimeo.arch.com/default-namespace" xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <pn:ChildNode2>value-2</pn:ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```
```xml
<!-- mimeo-output/mimeo-output-2.xml-->
<SomeEntity xmlns="http://mimeo.arch.com/default-namespace" xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <pn:ChildNode2>value-2</pn:ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```

When we would configure output format as `json` then it would produce:

```json
{
  "SomeEntity": {
    "@xmlns": "http://mimeo.arch.com/default-namespace",
    "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
    "ChildNode1": 1,
    "pn:ChildNode2": "value-2",
    "ChildNode3": true
  }
}
```
```json
{
  "SomeEntity": {
    "@xmlns": "http://mimeo.arch.com/default-namespace",
    "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
    "ChildNode1": 1,
    "pn:ChildNode2": "value-2",
    "ChildNode3": true
  }
}
```

#### CLI

```sh
mimeo SomeEntity-config.json
mimeo SomeEntity-config.xml
```

#### Python

##### `Mimeograph.process()`

This function generates data and consumes it.

```python
from mimeo import MimeoConfigFactory, Mimeograph

config = "SomeEntity-config.xml"
mimeo_config = MimeoConfigFactory.parse(config)
Mimeograph.process(mimeo_config)
```

##### `Mimeograph.generate()`

If you want to generate data and get it in a python representation,
you can use `Mimeograph.generate()` method. It will return dictionaries
(`json`) or `xml.etree.ElementTree.Element` instances (`xml`). 

```python
from mimeo import MimeoConfigFactory, Mimeograph

config = "SomeEntity-config.xml"
mimeo_config = MimeoConfigFactory.parse(config)
data = Mimeograph.generate(mimeo_config)
```

To consume data in a separated step you can make any modifications you want
and use `Mimeograph.consume()` method then.

### Mimeo Utils

Mimeo exposes several functions for data generation that will make it more useful for testing purposes.

**Template**
```json
{
  "count": 2,
  "model": {
    "SomeEntity": {
      "id": "{auto_increment}",
      "randomstring": "{random_str}",
      "randomint": "{random_int}"
    }
  }
}
```
```xml
<_template_>
    <count>2</count>
    <model>
        
        <SomeEntity>
            <id>{auto_increment}</id>
            <randomstring>{random_str}</randomstring>
            <randomint>{random_int}</randomint>
        </SomeEntity>
        
    </model>
</_template_>
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

**JSON Data**
```json
{
  "SomeEntity": {
    "id": "00001",
    "randomstring": "mCApsYZprayYkmKnYWxe",
    "randomint": 8
  }
}
```
```json
{
  "SomeEntity": {
    "id": "00002",
    "randomstring": "ceaPUqARUkFukZIPeuqO",
    "randomint": 99
  }
}
```


## Documentation

### Mimeo CLI

#### Mimeo Configuration arguments

When using Mimeo command line tool you can overwrite Mimeo Configuration properties:

| Short option | Long option         | Description                                                          |
|:------------:|:--------------------|:---------------------------------------------------------------------|
|     `-F`     | `--format`          | overwrite the `output/format` property                               |
|     `-o`     | `--output`          | overwrite the `output/direction` property                            |
|     `-x`     | `--xml-declaration` | overwrite the `output/xml_declaration` property                      |
|     `-i`     | `--indent`          | overwrite the `output/indent` property                               |
|     `-d`     | `--directory`       | overwrite the `output/directory_path` property                       |
|     `-f`     | `--file`            | overwrite the `output/file_name` property                            |
|     `-H`     | `--http-host`       | overwrite the `output/host` property                                 |
|     `-p`     | `--http-port`       | overwrite the `output/port` property                                 |
|     `-E`     | `--http-endpoint`   | overwrite the `output/endpoint` property                             |
|     `-U`     | `--http-user`       | overwrite the `output/username` property                             |
|     `-P`     | `--http-password`   | overwrite the `output/password` property                             |
|              | `--http-method`     | overwrite the `output/method` property                               |
|              | `--http-protocol`   | overwrite the `output/protocol` property                             |
|     `-e`     | `--http-env`        | overwrite the output http properties using a mimeo env configuration |
|              | `--http-envs-file`  | use a custom environments file (by default: mimeo.envs.json)         |

#### Logging arguments

| Short option | Long option | Description       |
|:------------:|:------------|:------------------|
|              | `--silent`  | disable INFO logs |
|              | `--debug`   | enable DEBUG mode |
|              | `--fine`    | enable FINE mode  |

### Mimeo Configuration

Mimeo configuration is defined in a JSON file using internal settings and data templates.

| Key                      |  Level   |      Required      |     Supported values     |    Default     | Description                                                                                                                                             |
|:-------------------------|:--------:|:------------------:|:------------------------:|:--------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `output`                 |  Config  |        :x:         |          object          |      ---       | Defines output details on how it will be consumed                                                                                                       |
| `output/direction`       |  Config  |        :x:         | `file`, `stdout`, `http` |     `file`     | Defines how output will be consumed                                                                                                                     |
| `output/format`          |  Config  |        :x:         |      `xml`, `json`       |     `xml`      | Defines output data format                                                                                                                              |
| `output/indent`          |  Config  |        :x:         |         integer          |     `null`     | Defines indent applied in output data                                                                                                                   |
| `output/xml_declaration` |  Config  |        :x:         |         boolean          |    `false`     | Indicates whether an xml declaration should be added to output data                                                                                     |
| `output/directory_path`  |  Config  |        :x:         |          string          | `mimeo-output` | For `file` direction - defines an output directory                                                                                                      |
| `output/file_name`       |  Config  |        :x:         |          string          | `mimeo-output` | For `file` direction - defines an output file name                                                                                                      |
| `output/method`          |  Config  |        :x:         |      `POST`, `PUT`       |     `POST`     | For `http` direction - defines a request method                                                                                                         |
| `output/protocol`        |  Config  |        :x:         |     `http`, `https`      |     `http`     | For `http` direction - defines a url protocol                                                                                                           |
| `output/host`            |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a url host                                                                                                               |
| `output/port`            |  Config  |        :x:         |         integer          |     `null`     | For `http` direction - defines a url port (can be empty)                                                                                                |
| `output/endpoint`        |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a url endpoint                                                                                                           |
| `output/username`        |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a username                                                                                                               |
| `output/password`        |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a password                                                                                                               |
| `vars`                   |  Config  |        :x:         |          object          |      ---       | Defines variables to be used in a Mimeo Template (read more in next section)                                                                            |
| `_templates_`            |  Config  | :heavy_check_mark: |          array           |      ---       | Stores templates for data generation                                                                                                                    |
| `count`                  | Template | :heavy_check_mark: |         integer          |      ---       | Indicates number of copies                                                                                                                              |
| `model`                  | Template | :heavy_check_mark: |          object          |      ---       | Defines data template to be copied                                                                                                                      |
| `context`                |  Model   |        :x:         |          object          |      ---       | Defines a context name that is internally used e.g. using `curr_iter()` and `get_key()` mimeo utils (by default model name is used as the context name) |

#### Mimeo Environment

To make `http` output directory easier to use, mimeo allows you to configure Mimeo Environments.
They are configured in a JSON file (by default: mimeo.envs.json) and support the following output details:
- `protocol`
- `host`
- `port`
- `username`
- `password`

Example
```json
{
    "local": {
        "host": "localhost",
        "port": 8000,
        "username": "admin",
        "password": "admin"
    },
    "dev": {
        "protocol": "https",
        "host": "11.111.11.111",
        "port": 8000,
        "username": "some-user",
        "password": "some-password"
    }
}
```

To use a specific Mimeo Environment you can use the following commands:
```sh
mimeo SomeEntity-config.json -e dev
mimeo SomeEntity-config.json -e dev --http-envs-file environments.json
```

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

You can use Mimeo Vars as partial values (unless they are defined as Mimeo Utils).

Example:
```json
{
  "vars": {
    "CUSTOM_VAR_1": "custom-value-1",
    "CUSTOM_VAR_2": 1,
    "CUSTOM_VAR_3": true,
    "CUSTOM_VAR_4": "{CUSTOM_VAR_2}",
    "CUSTOM_VAR_5": "{auto_increment}",
    "CUSTOM_VAR_6": {
      "_mimeo_util": {
        "_name": "random_int",
        "limit": 99
      }
    }
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
          "ChildNode7": "{CUSTOM_VAR_1}-with-suffix"
        }
      }
    }
  ]
}
```

#### Mimeo Special Fields

In Mimeo Template you can use so-called _special fields_.
Every field in a template can be stored in memory (_provided_) and used later as a value of other fields (_injected_).
To provide a special field, wrap its name with colons: [`:SomeField:`]. To inject, use additionally curly braces to
let interpreter know it should be rendered [`{:SomeField:}`].
They can be injected as partial values, similarly to Mimeo Vars.

Example
```json
{
  "_templates_": [
    {
      "count": 5,
      "model": {
        "SomeEntity": {
          ":ChildNode1:": "custom-value",
          "ChildNode2": "{:ChildNode1:}",
          "ChildNode3": "{:ChildNode1:}-with-suffix"
        }
      }
    }
  ]
}
```

#### Mimeo Utils

You can use several predefined functions to generate data. They can be used in a _raw_ format or _parametrized_.

##### Random String

Generates a random string value.

| Parameter | Supported values | Default |
|:---------:|:----------------:|:-------:|
|  length   |      `int`       |  `20`   |

###### Raw

Uses the default length: 20 characters.

```json
{
  "randomstring": "{random_str}"
}
```

###### Parametrized

Uses the customized length.

```json
{
  "randomstring": {
    "_mimeo_util": {
      "_name": "random_str",
      "length": 5
    }
  }
}
```

##### Random Integer

Generates a random integer value between `start` and `limit` parameters (inclusive).

| Parameter | Supported values | Default |
|:---------:|:----------------:|:-------:|
|   start   |      `int`       |   `1`   |
|   limit   |      `int`       |  `100`  |

###### Raw

Uses the default start (1) and limit (100) values.

```json
{
  "randominteger": "{random_int}"
}
```

###### Parametrized

Uses the customized limit.

```json
{
  "randominteger1": {
    "_mimeo_util": {
      "_name": "random_int",
      "start": 0
    }
  },
  "randominteger2": {
    "_mimeo_util": {
      "_name": "random_int",
      "limit": 5
    }
  },
  "randominteger3": {
    "_mimeo_util": {
      "_name": "random_int",
      "start": 0,
      "limit": 5
    }
  }
}
```

##### Random Item

Generates a random value from items provided.  
NOTICE: The raw form of this Mimeo Util will generate a blank string value (as same as no items parametrized).

| Parameter | Supported values | Default |
|:---------:|:----------------:|:-------:|
|   items   |      `list`      | `[""]`  |

###### Parametrized

```json
{
  "random": {
    "_mimeo_util": {
      "_name": "random_item",
      "items": ["value", 1, true]
    }
  }
}
```

##### Date

Generates a date value in format `YYYY-MM-DD`.

| Parameter  | Supported values | Default |
|:----------:|:----------------:|:-------:|
| days_delta |      `int`       |   `0`   |

###### Raw

Uses the today's date.

```json
{
  "Today": "{date}"
}
```

###### Parametrized

Uses the customized days delta.

```json
{
  "Yesterday": {
    "_mimeo_util": {
      "_name": "date",
      "days_delta": -1
    }
  },
  "Tomorrow": {
    "_mimeo_util": {
      "_name": "date",
      "days_delta": 1
    }
  }
}
```

##### Date Time

Generates a date time value in format `YYYY-MM-DD'T'HH:mm:SS`.

|   Parameter   | Supported values | Default |
|:-------------:|:----------------:|:-------:|
|  days_delta   |      `int`       |   `0`   |
|  hours_delta  |      `int`       |   `0`   |
| minutes_delta |      `int`       |   `0`   |
| seconds_delta |      `int`       |   `0`   |

###### Raw

Uses the current timestamp.

```json
{
  "Now": "{date_time}"
}
```

###### Parametrized

Uses the customized deltas.

```json
{
  "TomorrowThreeHoursLaterTwentyMinutesAgoTwoSecondsLater": {
    "_mimeo_util": {
      "_name": "date_time",
      "days_delta": 1,
      "hours_delta": 3,
      "minutes_delta": -20,
      "seconds_delta": 2
    }
  }
}
```

##### Auto Increment

Generates a next integer in context of a model (in nested templates it will use a separated context).

| Parameter | Supported values | Default  |
|:---------:|:----------------:|:--------:|
|  pattern  |      `str`       | `{:05d}` |

###### Raw

Uses a default pattern: **{:05d}** (an integer with 5 leading zeros).

```json
{
  "ID": "{auto_increment}"
}
```

###### Parametrized

Uses the string pattern provided.

```json
{
  "ID": {
    "_mimeo_util": {
      "_name": "auto_increment",
      "pattern": "MY_ID_{:010d}"
    }
  }
}
```

##### Current Iteration

Generates a value of the current iteration in a Mimeo Template context.

| Parameter | Supported values |      Default      |
|:---------:|:----------------:|:-----------------:|
|  context  |      `str`       | a current context |

###### Raw

Uses the current context.

```json
{
  "ID": "{curr_iter}"
}
```

###### Parametrized

Uses a specific Mimeo Model context (model name when `context` is not configured).

```json
{
  "Parent": {
    "_mimeo_util": {
      "_name": "curr_iter",
      "context": "SomeEntity"
    }
  }
}
```

##### Key

Generates a key unique across all Mimeo Models and being the same within a single Mimeo Model context.

| Parameter | Supported values |              Default               |
|:---------:|:----------------:|:----------------------------------:|
|  context  |      `str`       |         a current context          |
| iteration |      `int`       | a current iteration of the context |

###### Raw

Uses a key from the current context and iteration.

```json
{
  "ID": "{key}"
}
```

###### Parametrized

Uses a key from the specific context and iteration.  
When context is indicated and iteration is not, then the current iteration **of the indicated context** is being used.

```json
{
  "SomeEntity2": {
    "_mimeo_util": {
      "_name": "key",
      "context": "SomeEntity",
      "iteration": "{curr_iter}"
    }
  }
}
```

##### City

Generates a city name.

| Parameter | Supported values | Default |
|:---------:|:----------------:|:-------:|
|  unique   |      `bool`      | `True`  |
|  country  |      `str`       | `None`  |

###### Raw

By default city names will be unique across a Mimeo Context.

```json
{
  "City": "{city}"
}
```

###### Parametrized

Uses country (name, iso2, iso3) and `unique` flag to generate a city name.

```json
{
  "CityWithDuplicates": {
    "_mimeo_util": {
      "_name": "city",
      "unique": false
    }
  },
  "CityOfCountryName": {
    "_mimeo_util": {
      "_name": "city",
      "country": "United Kingdom"
    }
  },
  "CityOfCountryISO2": {
    "_mimeo_util": {
      "_name": "city",
      "country": "GB"
    }
  },
  "CityOfCountryISO3": {
    "_mimeo_util": {
      "_name": "city",
      "country": "GBR"
    }
  },
  "CityOfCountryWithDuplicates": {
    "_mimeo_util": {
      "_name": "city",
      "country": "United Kingdom",
      "unique": false
    }
  }
}
```

##### Country

Generates a country name (by default), iso2 or iso3.

| Parameter |       Supported values       | Default  |
|:---------:|:----------------------------:|:--------:|
|  unique   |            `bool`            |  `True`  |
|   value   | `"name"`, `"iso3"`, `"iso2"` | `"name"` |
|  country  |            `str`             |  `None`  |

###### Raw

By default country names will be unique across a Mimeo Context.

```json
{
  "Country": "{country}"
}
```

###### Parametrized

It can generate:
- country iso3 or iso 2 instead of name
- country with duplicates
- country name for a provided iso3 or iso2
- country iso2 for a provided name or iso3
- country iso3 for a provided name or iso2

When the `country` param is provided then the `unique` flag is ignored.

```json
{
  "CountryNameWithDuplicates": {
    "_mimeo_util": {
      "_name": "country",
      "unique": false
    }
  },
  "CountryISO2": {
    "_mimeo_util": {
      "_name": "country",
      "value": "iso2"
    }
  },
  "CountryISO3": {
    "_mimeo_util": {
      "_name": "country",
      "value": "iso3"
    }
  },
  "CountryNameForISO3": {
    "_mimeo_util": {
      "_name": "country",
      "country": "GBR"
    }
  },
  "CountryISO2ForName": {
    "_mimeo_util": {
      "_name": "country",
      "value": "iso2",
      "country": "United Kingdom"
    }
  }
}
```

##### Currency

Generates a currency code (by default) or name.

| Parameter |  Supported values  | Default  |
|:---------:|:------------------:|:--------:|
|  unique   |       `bool`       | `False`  |
|   value   | `"code"`, `"name"` | `"code"` |
|  country  |       `str`        |  `None`  |

###### Raw

By default city names will _NOT_ be unique across a Mimeo Context.

```json
{
  "Currency": "{currency}"
}
```

###### Parametrized

It can generate:
- unique currencies
- currency name instead of code
- currency code or name of a specific country (using iso3, iso2 or name)

When the `country` param is provided then the `unique` flag is ignored.

```json
{
  "UniqueCurrencyCode": {
    "_mimeo_util": {
      "_name": "currency",
      "unique": true
    }
  },
  "CurrencyName": {
    "_mimeo_util": {
      "_name": "currency",
      "value": "name"
    }
  },
  "CurrencyCodeForCountryISO3": {
    "_mimeo_util": {
      "_name": "currency",
      "country": "GBR"
    }
  },
  "CurrencyNameForCountryISO2": {
    "_mimeo_util": {
      "_name": "currency",
      "value": "name",
      "country": "GB"
    }
  },
  "CurrencyNameForCountryName": {
    "_mimeo_util": {
      "_name": "currency",
      "value": "name",
      "country": "United Kingdom"
    }
  }
}
```

##### First Name

Generates a first name.

| Parameter |      Supported values      | Default  |
|:---------:|:--------------------------:|:--------:|
|  unique   |           `bool`           |  `True`  |
|    sex    | `M`, `Male`, `F`, `Female` |  `None`  |

###### Raw

By default first names will be unique across a Mimeo Context.

```json
{
  "FirstName": "{first_name}"
}
```

###### Parametrized

Uses sex (`M` / `Male` / `F` / `Female`) and `unique` flag to generate a first name.

```json
{
  "FirstNameWithDuplicates": {
    "_mimeo_util": {
      "_name": "first_name",
      "unique": false
    }
  },
  "MaleFirstName": {
    "_mimeo_util": {
      "_name": "first_name",
      "sex": "M"
    }
  },
  "FemaleFirstName": {
    "_mimeo_util": {
      "_name": "first_name",
      "sex": "F"
    }
  },
  "MaleFirstNameWithDuplicates": {
    "_mimeo_util": {
      "_name": "first_name",
      "sex": "M",
      "unique": false
    }
  }
}
```

##### Last Name

Generates a last name.

| Parameter | Supported values | Default  |
|:---------:|:----------------:|:--------:|
|  unique   |      `bool`      |  `True`  |

###### Raw

By default last names will be unique across a Mimeo Context.

```json
{
  "LastName": "{last_name}"
}
```

###### Parametrized

Uses `unique` flag to generate a last name.

```json
{
  "LastNameWithDuplicates": {
    "_mimeo_util": {
      "_name": "last_name",
      "unique": false
    }
  }
}
```


## License

MIT


## Authors

- [@TomaszAniolowski](https://www.github.com/TomaszAniolowski)


## Acknowledgements

 - [SimpleMaps.com](https://simplemaps.com/data/world-cities) (Cities & countries data)
 - [@hadley/data-baby-names](https://github.com/hadley/data-baby-names/) (Forenames data)
 - [@fivethirtyeigh/data/most-common-name](https://github.com/fivethirtyeight/data/tree/master/most-common-name) (Surnames data)
 - [@datasets/currency-codes](https://github.com/datasets/currency-codes/) (Currencies data)
