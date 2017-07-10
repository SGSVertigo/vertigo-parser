# vertigoIMU Parser

This repo contains a Python based parser for the binary logfiles produced by
vertigoIMU. This is useful since sometimes the logger cannot complete the log
conversion on-board (e.g., battery removed or depleted).

## Usage

1. Clone the repository and `cd` into it
2. Create a virtualenv with `$ virtualenv venv`
3. Install requirements using `$ pip install -r requirements.txt`
4. Put the binary log and the meta file (e.g., `vtg_log0.bin` and
`vtg_log0.meta.bin`) into the working directory.
5. Run using `$ python parse.py vtg_log0.bin`
6. The output will be created in `vtg_log0.csv`. You are done.

## Authorship

Copyright Jon Sowman 2017. All rights reserved.
