[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)


[![Formatting Checks](https://github.com/SDEGroup5/github-actions/actions/workflows/yapf.yaml/badge.svg?event=check_run)](https://github.com/SDEGroup5/github-actions/actions/workflows/yapf.yaml)

[![Quality Checks](https://github.com/SDEGroup5/github-actions/actions/workflows/ruff.yml/badge.svg?event=check_run)](https://github.com/SDEGroup5/github-actions/actions/workflows/ruff.yml)

[![Pylint](https://github.com/SDEGroup5/github-actions/actions/workflows/pylint.yml/badge.svg?event=check_run)](https://github.com/SDEGroup5/github-actions/actions/workflows/pylint.yml)

[![Python application](https://github.com/SDEGroup5/github-actions/actions/workflows/python-app.yml/badge.svg?event=release)](https://github.com/SDEGroup5/github-actions/actions/workflows/python-app.yml)

[![Backend Docker Image](https://github.com/SDEGroup5/github-actions/actions/workflows/backend-image.yml/badge.svg?event=registry_package)](https://github.com/SDEGroup5/github-actions/actions/workflows/backend-image.yml)

[![Frontend Docker Image](https://github.com/SDEGroup5/github-actions/actions/workflows/frontend-image.yml/badge.svg?event=registry_package)](https://github.com/SDEGroup5/github-actions/actions/workflows/frontend.yml)

# Github Actions
A project to show how Github Action works.

## Project setup requirements

Make sure to have the following dependencies installed on the system: `python3-dev`, `libpq-dev`.

In case of problems regarding the `psycopg2` package, you can install the compiled binary instead.
In such case, run this command to change the `requirements.txt` file:

```sh
sed -i '/psycopg2==2\.9\.13/c\psycopg2-binary==2.9.13' requirements.txt
```

Run the make file with:

```sh
make init
```

Then enter the Python Virtual Environment with:

```sh
source .venv/bin/activate
```

## Authors
- Caraffini Lorenzo @LorenzoCaraffini
- Palmieri Filippo @FilizZPalm
- Radice Lorenzo @ozneroL541
- Schievano Matteo @FireStoat3
- Stanicel David @Oziator

## License
Copyright (C) 2026  Caraffini Lorenzo, Palmieri Filippo, Radice Lorenzo, Schievano Matteo, Stanicel David

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
