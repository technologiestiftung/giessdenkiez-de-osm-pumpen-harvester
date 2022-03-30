![](https://img.shields.io/badge/Build%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiesitftung%20Berlin-blue)

# Giess den Kiez Pumpen aggregation from OSM

This is a Docker based GitHub Action to aggregate pumps data from open street maps and to store them in a geojson-file. 

The aggregated data is used to provide locations and information about the Berlin street pumps in the frontend of [Gieß den Kiez](https://github.com/technologiestiftung/giessdenkiez-de).
The [Overpass API](http://overpass-api.de) for OSM is used to retrieve the data, by fetching all nodes with tag "man_made"="water_well" and "description"="Berliner Straßenbrunnen". The corresponding query is defined and can be modified in the script *fetch.py*. 
The data obtained in this way is further processed and the raw OSM data is filtered. In *utils.py*, all attributes are dropped that are theoretically still available in the OSM data, but which we do not need. By adding the respective attributes to the filter list, they can be included in the final data set.


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
        # use tags if you want to fix on a specific version
        # e.g 
        # uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@1.2.0
        # use master if you like to gamble
        uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@master
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

**Achtung!:** For our case these files get added to the repo again. Therefore we need to use two other actions.

- A source checkout action.
- A add and commit action.

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
      - name: Checkout
        uses: actions/checkout@v2
      - name: Pumps data generate step
        uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@master
        id: pumps
        with:
          outfile-path: "out/pumps.geojson"
      # Use the output from the `pumps` step
      - name: File output
        run: echo "The file was written to ${{ steps.pumps.outputs.file }}"
        # https://github.com/marketplace/actions/add-commit?version=v4.4.0
      - name: Add & Commit
        uses: EndBug/add-and-commit@v4.4.0 # You can change this to use a specific version
        with:
          add: out
          author_name: you
          author_email: you@example.com
          message: "Update ${{ steps.pumps.outputs.file }}"
        env:
          # This is necessary in order to push a commit to the repo
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Leave this line unchanged
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
  <tr>
    <td align="center"><a href="https://fabianmoronzirfas.me/"><img src="https://avatars.githubusercontent.com/u/315106?v=4?s=64" width="64px;" alt=""/><br /><sub><b>Fabian Morón Zirfas</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=ff6347" title="Code">💻</a> <a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=ff6347" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/Lisa-Stubert"><img src="https://avatars.githubusercontent.com/u/61182572?v=4?s=64" width="64px;" alt=""/><br /><sub><b>Lisa-Stubert</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=Lisa-Stubert" title="Code">💻</a> <a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=Lisa-Stubert" title="Documentation">📖</a></td>
  </tr>
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