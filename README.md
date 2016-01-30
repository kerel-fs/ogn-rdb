# OGN Receiver Database

A parser for <http://wiki.glidernet.org/list-of-receivers>,
returns the list-of-receivers in a machine-readable format (see [data format](#data-format)).

## Installation

- Install dependencies

  ```
  pip install -r requirements.txt
  ```

## Usage

- mkreceiverjson.py

  Fetch the list-of-receivers from wiki.glidernet.org and output it
  into a (machine-readable) file `receivers.json`.

  ```
  mkreceiverjson.py --out receivers.json --obfuscate
  ```

- mkstatistics.py

  Generate some statistics from `receivers.json`.

  ```
  mkstatistics.py --in receivers.json
  ```

## Data format

### receiver-wiki.json

```
{ 'receivers':
  [
    {
      'callsign': string,
      'description': string,
      'photos': [string, ...],
      'contact': string,
      'country': string
    },
    ...
  ],
  },
  'timestamp': isoformat
}
```

# License

Licensed under the [AGPLv3](LICENSE) or later.
