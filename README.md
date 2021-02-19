# CloudFoundry Application logs Alert

[![Codeship Status for kumbasar/cf-logs-alert](https://app.codeship.com/projects/3112835d-71ee-43c3-8a6d-7cdc27e3946e/status?branch=main)](https://app.codeship.com/projects/422129)
![cf-logs-alert](https://github.com/kumbasar/cf-logs-alert/workflows/cf-logs-alert/badge.svg)

A notification tool for cloud foundry applications 

## Start local test email server

```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```

## Build and run Docker container

```bash
docker build -t cf-logger . 
docker run -t cf-logger   
```

## Proxy

```bash
export HTTPS_PROXY=<HTTPS_PROXY>
export HTTP_PROXY=<HTTP_PROXY>

./main.py
```

Or

```bash
HTTPS_PROXY=<HTTPS_PROXY> ./main.py
```