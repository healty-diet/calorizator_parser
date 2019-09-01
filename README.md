# Calorizator site parser

This program is designed to parse data about food energy value from the [calorizator.ru](http://calorizator.ru/).

## Legal note

This software is designed _only_ for personal use and supposed to be an alternative form of web-site using. All the data obtained with this software belongs to [calorizator.ru](http://calorizator.ru/). In order to use collected data in your project or for business you should contact the site administration first to obtain the approval.

Data is parsed to the json format and written to the file provided by the user.

## Examples

Example of the result json entry:

```json
{
  "7up": {
    "protein": 0,
    "fat": 0,
    "carbohydrates": 8.7,
    "calories": 38
  }
}
```

## Usage

```sh
calorizator_parser [-h] --output OUTPUT
```

## LICENSE

Calorizator parser is licensed under the MIT License.
See [LICENSE] for details.

[LICENSE]: https://github.com/popzxc/calorizator_parser/blob/master/LICENSE
