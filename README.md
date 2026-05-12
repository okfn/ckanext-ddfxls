[![CKAN 2.11 Tests](https://github.com/okfn/ckanext-ddfxls/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/okfn/ckanext-ddfxls/actions/workflows/test.yml)

# ckanext-ddfxls

A datastore dump for XLS files.  
Note: This depends on [CKAN#9345](https://github.com/ckan/ckan/pull/9345) to be merged.  

<img src="/extras/imgs/shot.png" alt="screenshot" width="600">


## Requirements

This extensions requires `openpyxl`. Check the [requirements.txt](requirements.txt) file for more details.  

## CKAN versions
Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.9             | no            |
| 2.10            | no            |
| 2.11            | yes           |


## Usage

Add `ddfxls` to the `ckan.plugins` setting in your CKAN config file

## Config settings

None at present

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
