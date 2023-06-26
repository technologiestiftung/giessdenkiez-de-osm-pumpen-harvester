![](https://img.shields.io/badge/Built%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiestiftung%20Berlin-blue)

# Giess den Kiez Pumpen aggregation from OSM

This is a Docker based GitHub Action to aggregate pumps data from OpenStreetMap and to store them in a geojson file.

The aggregated data is used to provide locations and information about the street pumps in the frontend of [Gieß den Kiez](https://github.com/technologiestiftung/giessdenkiez-de).
The [Overpass API](http://overpass-api.de) for OSM is used to retrieve the data, by fetching all nodes with tag `"man_made"="water_well"` and `"description"="Berliner Straßenbrunnen"`.

The corresponding query is defined in the script [fetch.py](/fetch.py). It can be overriden by providing a custom overpass query statement.

The data obtained in this way is further processed and the raw OSM data is filtered. In _utils.py_, all attributes are dropped that are theoretically still available in the OSM data, but which we do not need. By adding the respective attributes to the filter list, they can be included in the final data set.

## Inputs

### `outfile-path`

**Required** The path where the GeoJSON file should be written to. Default `"public/data/pumps.geojson"`.

### `query`

A custom overpass query statement to retrieve pumps from OpenStreetMap. When omitted, the action will retrieve Berlin pumps.

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
        # use tags if you want to fix on a specific version
        # e.g
        # uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@1.2.0
        # use master if you like to gamble
        uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@master
        id: pumps
        with:
          outfile-path: "out/pumps.geojson"
          # Pass "query" argument to specify custom overpass query string (see example below for the city of Magdeburg)
          # query: '[out:json][bbox:52.0124,11.4100, 52.2497,11.8330];(node["man_made"="water_well"];);out;>;out;'
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
          # Pass "query" argument to specify custom overpass query string (see example below for the city of Magdeburg)
          # query: '[out:json][bbox:52.0124,11.4100, 52.2497,11.8330];(node["man_made"="water_well"];);out;>;out;'
      # Use the output from the `hello` step
      - name: File output
        run: echo "The file was written to ${{ steps.pumps.outputs.file }}"
```

**Achtung!:** For our case these files get pushed to a Supabase storage bucket. Therefore we need to use another script action.

See a full example workflow below.

```yml
name: Full Pumps CI
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
        uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@master
        id: pumps
        with:
          outfile-path: "out/pumps.geojson"
          query: '[out:json][bbox:52.0124,11.4100, 52.2497,11.8330];(node["man_made"="water_well"];);out;>;out;'
      # Use the output from the `pumps` step
      - name: File output
        run: echo "The file was written to ${{ steps.pumps.outputs.file }}"
        # https://github.com/marketplace/actions/add-commit?version=v4.4.0
      - name: Upload file to supabase
        run: |
          getStatusCode=$(curl -s -o /dev/null -w "%{http_code}" \
            -X GET \
            ${{ vars.SUPABASE_URL_TEST }}/storage/v1/object/info/public/${{ vars.SUPABASE_DATA_ASSETS_BUCKET_TEST }}/pumps.geojson)
          if [ "$getStatusCode" = "200" ]; then
            putStatusCode=$(curl -s -o /dev/null -w "%{http_code}" \
              -X PUT \
              -H "Authorization: Bearer ${{ secrets.SUPABASE_ACCESS_TOKEN_TEST }}" \
              -H "Content-Type: application/geo+json" \
              -d "@${{ steps.pumps.outputs.file }}" \
              ${{ vars.SUPABASE_URL_TEST }}/storage/v1/object/${{ vars.SUPABASE_DATA_ASSETS_BUCKET_TEST }}/pumps.geojson)
            if [ "$putStatusCode" = "200" ]; then
              echo "Uploading to Supabase successful"
            else
              echo "Uploading to Supabase failed"
              exit 1
            fi
          else
            postStatusCode=$(curl -s -o /dev/null -w "%{http_code}" \
              -X POST \
              -H "Authorization: Bearer ${{ secrets.SUPABASE_ACCESS_TOKEN_TEST }}" \
              -H "Content-Type: application/geo+json" \
              -d "@${{ steps.pumps.outputs.file }}" \
              ${{ vars.SUPABASE_URL_TEST }}/storage/v1/object/${{ vars.SUPABASE_DATA_ASSETS_BUCKET_TEST }}/pumps.geojson)
            if [ "$postStatusCode" = "200" ]; then
              echo "Uploading to Supabase successful"
            else
              echo "Uploading to Supabase failed"
              exit 1
            fi
          fi         
```

## Development

See also https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action

### Python

Run the script with `python3 harvester/main.py path/to/out/file.geojson`

### Docker

Build the container and run it.

```bash
mkdir out
docker build --tag technologiestiftung/giessdenkiez-de-osm-pumpen-harvester .
docker run -v $PWD/out:/scripts/out technologiestiftung/giessdenkiez-de-osm-pumpen-harvester path/scripts/out/outfile.json
```

### Test

```bash
pytest
pytest --cov=harvester --cov-fail-under 75 --cov-config=.coveragerc
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://fabianmoronzirfas.me/"><img src="https://avatars.githubusercontent.com/u/315106?v=4?s=64" width="64px;" alt="Fabian Morón Zirfas"/><br /><sub><b>Fabian Morón Zirfas</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=ff6347" title="Code">💻</a> <a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=ff6347" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Lisa-Stubert"><img src="https://avatars.githubusercontent.com/u/61182572?v=4?s=64" width="64px;" alt="Lisa-Stubert"/><br /><sub><b>Lisa-Stubert</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=Lisa-Stubert" title="Code">💻</a> <a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=Lisa-Stubert" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vogelino"><img src="https://avatars.githubusercontent.com/u/2759340?v=4?s=64" width="64px;" alt="Lucas Vogel"/><br /><sub><b>Lucas Vogel</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=vogelino" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JensWinter"><img src="https://avatars.githubusercontent.com/u/6548550?v=4?s=64" width="64px;" alt="Jens Winter-Hübenthal"/><br /><sub><b>Jens Winter-Hübenthal</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=JensWinter" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

<table>
  <tr>
    <td>
      <a src="https://citylab-berlin.org/en/start/">
        <br />
        <br />
        <img width="200" src="https://logos.citylab-berlin.org/logo-citylab-berlin.svg" />
      </a>
    </td>
    <td>
      A project by: <a src="https://www.technologiestiftung-berlin.de/en/">
        <br />
        <br />
        <img width="150" src="https://logos.citylab-berlin.org/logo-technologiestiftung-berlin-en.svg" />
      </a>
    </td>
    <td>
      Supported by:
      <br />
      <br />
      <img width="120" src="https://logos.citylab-berlin.org/logo-berlin.svg" />
    </td>
  </tr>
</table>
