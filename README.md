# Giessdenkiez.de Pumpen aggregation from OSM

This is a Docker based GitHub Action to aggregate pumps data from open street maps.


## Inputs 

### `outfile-path`

**Required** The path where the GeoJSON file should be written to. Default `"public/data/pumps.geojson"`.

## Outputs

### `file`

The path to where the file was written.

## Example Usage

### Public repo

File: `.github/workflows/main.yml`

```yml
on:
  workflow_dispatch:
  schedule:
    # every sunday morning at 4:00
    - cron: "0 4 * * 0"

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to aggregate pumps data from open street maps
    steps:
      - name: Pumps data generate step
        uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@1.0.0
        id: pumps
        with:
          outfile-path: "out/pumps.geojson"
      # Use the output from the `pumps` step
      - name: File output
        run: echo "The file was written to ${{ steps.pumps.outputs.file }}"
```

### Your own Private Repo

File: `.github/workflows/main.yml`

```yml
on:
  workflow_dispatch:
  schedule:
    # * is a special character in YAML so you have to quote this string
    - cron: "0 4 * * 0"

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to aggregate pumps data from open street maps
    steps:
      # To use this repository's private action,
      # you must check out the repository
      - name: Checkout
        uses: actions/checkout@v2
      - name: Pumps data generate step
        uses: ./ # Uses an action in the root directory
        id: pumps
        with:
          outfile-path: "out/pumps.geojson"
      # Use the output from the `hello` step
      - name: File output
        run: echo "The file was written to ${{ steps.pumps.outputs.file }}"
```

## Development

See also https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action

### Python

Run the script with `python3 fetch_osm_pumps.py path/to/out/file.geojson`

### Docker  

Build the container and run it.

```bash
docker build --tag technologiestiftung/giessdenkiez-de-osm-pumpen-harvester .
docker run -v $PWD/out:/scripts/out technologiestiftung/giessdenkiez-de-osm-pumpen-harvester path/to/outfile.json
```

### Test

- tbd