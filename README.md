# CloudFoundry Application logs Alert

[![Codeship Status for kumbasar/cf-logs-alert](https://app.codeship.com/projects/3112835d-71ee-43c3-8a6d-7cdc27e3946e/status?branch=main)](https://app.codeship.com/projects/422129)
![cf-logs-alert](https://github.com/kumbasar/cf-logs-alert/workflows/cf-logs-alert/badge.svg)

A notification tool for cloud foundry applications 

## Start local test email server

```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```

## Docker container build and run

```bash
docker build -t cf-logger . 
docker run -t cf-logger   
```

## Proxy Configuration

```bash
export HTTPS_PROXY=<HTTPS_PROXY>
export HTTP_PROXY=<HTTP_PROXY>

./main.py
```

or

```bash
./main.py --proxy <HTTPS_PROXY>
```

## Test

**Startup**

```bash
docker-compose -up --build
```

Example output:

```bash
mailserver_1  | ---------- MESSAGE FOLLOWS ----------
mailserver_1  | b'Content-Type: text/plain; charset="utf-8"'
mailserver_1  | b'Content-Transfer-Encoding: 7bit'
mailserver_1  | b'MIME-Version: 1.0'
mailserver_1  | b'Subject: CF log alert'
mailserver_1  | b'From: kumbasar@localhost'
mailserver_1  | b'To: volkan@localhost'
mailserver_1  | b'X-Peer: 172.21.0.3'
mailserver_1  | b''
mailserver_1  | b'Org/space: welcome/dev'
mailserver_1  | b'App: roster'
mailserver_1  | b'Key: error'
mailserver_1  | b'Log: origin: "rep"'
mailserver_1  | b'eventType: ContainerMetric'
mailserver_1  | b'timestamp: 1613823966400034322'
mailserver_1  | b'containerMetric {'
mailserver_1  | b'  applicationId: "85d139e7-9fb3-4041-b80a-5970f624a415"'
mailserver_1  | b'  instanceIndex: 0'
```

**Shutdown**

```bash
docker-compose -down
```
