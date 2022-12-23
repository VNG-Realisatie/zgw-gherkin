# systeem-tests

## Run locally

1. Create a venv and activate
2. Install packages
```shell
pip install -r requirements.txt
```
3. Run behave
```shell
behave
```

## Run on docker

1. Build image (change the tag as needed)
```shell
docker build -t systeem-tests:v0.1 .
```
2. Run a container
```shell
docker run --name test -d -e TOKEN=${YOUR_TOKEN} systeem-tests:v0.1
```
3. Retrieve logs
```shell
docker logs test
```

Alternativly you can run command 2 without the `-d` flag.
