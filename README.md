
# Mimeo (Mimeograph)

**Mimeo** is a tool generating custom data based on a template. It can be useful in for developers, testers or even business analists in their daily work.



## Installation

Install Mimeo with pip

```sh
pip install mimeograph
```
    
## Usage/Examples

```sh
mimeo SomeEntity-config.json
```

### Basic templates

*Notice: Mimeo templates are JSON objects included in Mimeo configuration. More about it you will learn in the **Documentation** section.*

**Template**
```json
{
  "count": 2,
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
```

**XML Data**
```xml
<SomeEntity xmlns="http://data-generator.arch.com/default-namespace" xmlns:pn="http://data-generator.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <ChildNode2>value-2</ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```
```xml
<SomeEntity xmlns="http://data-generator.arch.com/default-namespace" xmlns:pn="http://data-generator.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <ChildNode2>value-2</ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```

### Additional features

Mimeo exposes several functions for data generation that will make it more useful for testing purposes.

**Template**
```json
{
  "count": 2,
  "model": {
    "attributes": {
      "xmlns": "http://data-generator.arch.com/default-namespace"
    },
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
<SomeEntity xmlns="http://data-generator.arch.com/default-namespace">
    <id>00001</id>
    <randomstring>mCApsYZprayYkmKnYWxe</randomstring>
    <randomint>8</randomint>
</SomeEntity>
```
```xml
<SomeEntity xmlns="http://data-generator.arch.com/default-namespace">
    <id>00003</id>
    <randomstring>ceaPUqARUkFukZIPeuqO</randomstring>
    <randomint>2</randomint>
</SomeEntity>
```

You can find more configuration examples in the `examples` folder.
## Documentation

### Mimeo configuration

Mimeo configuration is defined in a json file using internal settings and data templates.

|               Key               |  Level   |      Required      | Supported values |    Default     | Description                                                              |
|:-------------------------------:|:--------:|:------------------:|:----------------:|:--------------:|--------------------------------------------------------------------------|
|         `output_format`         |  Config  |        :x:         |      `xml`       |     `xml`      | Defines output data format                                               |
|        `output_details`         |  Config  |        :x:         |      object      |      ---       | Defines output details on how it will be consumed                        |
|   `output_details/direction`    |  Config  |        :x:         |  `file`, `raw`   |     `file`     | Defines how output will be consumed                                      |
| `output_details/directory_path` |  Config  |        :x:         |      string      | `mimeo-output` | For `file` direction - defines an output directory                       |
|   `output_details/file_name`    |  Config  |        :x:         |      string      | `mimeo-output` | For `file` direction - defines an output file name                       |
|            `indent`             |  Config  |        :x:         |     integer      |     `null`     | Defines indent applied in output data                                    |
|        `xml_declaration`        |  Config  |        :x:         |     boolean      |    `false`     | Indicates whether an xml declaration should be added to output data      |
|          `_templates_`          |  Config  | :heavy_check_mark: |      array       |      ---       | Stores templates for data generation                                     |
|             `count`             | Template | :heavy_check_mark: |     integer      |      ---       | Indicates number of copies                                               |
|             `model`             | Template | :heavy_check_mark: |      object      |      ---       | Defines data template to be copied                                       |
|          `attributes`           |  Model   |        :x:         |      object      |      ---       | Defines attributes applied on the root node (mostly used for namespaces) |


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@TomaszAniolowski](https://www.github.com/TomaszAniolowski)

