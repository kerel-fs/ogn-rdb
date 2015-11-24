# OGN Receiver Database

A parser for <http://wiki.glidernet.org/list-of-receivers>,
it returns json-formatted output.

## Modules
### mkreceiverjson.py
Parse the list of receivers from a dump of wiki.glidernet.org.
The retrieved information is saved as `receiver-wiki.json`.

### mkstatistics.py
Generate some statistics for stations in a `receiver-wiki.json`-file.

### Library
- wikidotcrawler.py

## Data Format
### receiver-wiki.json

```
{'receivers': {
    id: {'description': string,
         'photos': [string, ...],
         'contact': string,
         'country': string
        },
    ...
  },
  'timestamp': isoformat
}
```

# License

Licensed under the [AGPLv3](LICENSE) or later.
