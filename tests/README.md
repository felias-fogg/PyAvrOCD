# Running tests


Run tests in root folder using:
`poetry run python3 -m unittest`


Run integration test in root folder (probably only works on POSIX
OSs). First start the server in one terminal window:
```
tests/serv.sh <mcu>
```
Then start the integration tests in another window (root directory)
`poetry run python3 -m tests.integration_test -d <mcu> -c <clock in MHz>`

Afterwards, you need to kill the `serv.sh` script with CTRL-C
