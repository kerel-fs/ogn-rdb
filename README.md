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

### receivers.json

Specification: [receiverlist-schema-0.2.0](receiverlist-schema-0.2.0.json)

Example:
```
{ 'receivers':
  [
    {
      'callsign': "N0CALL",
      'description': "An OGN receiver located on planet earth",
      'photos': ["https://example.com/ogn/receiver-photo.jpg"],
      'contact': "ogn@example.com",
      'country': "None"
    },
  ],
  },
  'timestamp': "2016-02-04T11:11:11",
  'version': '0.2.0'
}
```

## Data analysis ([jq](https://stedolan.github.io/jq/) required)

Show all receiver callsigns, grouped by country:
```
cat receivers.json | jq ".receivers | group_by(.country) | map({(.[0].country): [.[].callsign]})"
```

## License

Licensed under the [AGPLv3](LICENSE) or later.
