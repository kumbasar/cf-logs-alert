# Cloud Foundry Application Alerter

This tool fetches all log streams from a Cloud Foundry target (`org`/`space`) and posts an email notification if it parses a trigger keyword. 

[![Codeship Status for kumbasar/cf-logs-alert](https://app.codeship.com/projects/3112835d-71ee-43c3-8a6d-7cdc27e3946e/status?branch=main)](https://app.codeship.com/projects/422129)
![cf-logs-alert](https://github.com/kumbasar/cf-logs-alert/workflows/cf-logs-alert/badge.svg)


## Usage

Before starting the tool, first update the `config.json` file according to your settings. All input parameters are listed in the table below.

Parameter | Info | 
------ | ------|
`space`|  CF space value
`org`|  CF org value
`user`|  CF username
`password`|  CF password
`api`|  CF target URL
`smtp`| SMTP IP address or hostname
`port`|  SMTP port #
`sender_email`|  Email poster
`receiver_email`|  Receiver list
`keys`| Notifaction keyword list

Execute the below commands to install the dependencies:

```bash
pip3 install -r requirements.txt
chmod +x main.py
```

To start the alert tool:

```bash
./main.py 
```

Also, you might want to build and run the tool in a Docker container. If so, you can check out the provided `Dockerfile` as an example.

In short, to build and run the tool via Docker:

```bash
docker build -t cf-logger . 
docker run -t cf-logger   
```

## Proxy Configuration

You can set your proxy settings as follows:

```bash
export HTTPS_PROXY=<HTTPS_PROXY>
export HTTP_PROXY=<HTTP_PROXY>

./main.py
```

or

```bash
./main.py --proxy <HTTPS_PROXY>
```

##  Optional: Setup a email server

For testing, you can setup a dummy email server as follows.

First, update the `config.json` file as follows:

```JSON
[...]
"email": {
    "smtp": "localhost",
    "port": "1025",
    "sender_email": "test@localhost",
    "receiver_email": "test@localhost"
}
[...]
```

Execute the test server:

```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```

In a different terminal, start the tool.

```bash
./main.py
```

Also, you can use the `docker compose` framework for testing. Just, set the `smtp` value to `mailserver`. 

@`config.json`:
```JSON
[...]
    "smtp": "mailserver",
[...]
```

Execute below command to build and start up the containers.

```bash
docker-compose up --build
```

Example alert console output:

```bash
mailserver_1  | ---------- MESSAGE FOLLOWS ----------
mailserver_1  | b'Content-Type: text/plain; charset="utf-8"'
mailserver_1  | b'Content-Transfer-Encoding: 7bit'
mailserver_1  | b'MIME-Version: 1.0'
mailserver_1  | b'Subject: CF log alert'
mailserver_1  | b'From: kumbasar@localhost'
mailserver_1  | b'To: volkan@localhost'
mailserver_1  | b'X-Peer: 172.19.0.3'
mailserver_1  | b''
mailserver_1  | b'Org/space: welcome/dev'
mailserver_1  | b'App: roster'
mailserver_1  | b'Key: eventType'
mailserver_1  | b'Log: origin: "rep"'
mailserver_1  | b'eventType: ContainerMetric'
mailserver_1  | b'timestamp: 1615139019420518865'
mailserver_1  | b'containerMetric {'
mailserver_1  | b'  applicationId: "85d139e7-9fb3-4041-b80a-5970f624a415"'
mailserver_1  | b'  instanceIndex: 0'
mailserver_1  | b'  cpuPercentage: 1.0301370119722197'
mailserver_1  | b'  memoryBytes: 375887877'
mailserver_1  | b'  diskBytes: 163287040'
mailserver_1  | b'  memoryBytesQuota: 786432000'
mailserver_1  | b'  diskBytesQuota: 1073741824'
mailserver_1  | b'}'
mailserver_1  | b'deployment: "kubecf"'
mailserver_1  | b'job: "diego-cell-loggr-forwarder-agent"'
mailserver_1  | b'index: "diego-cell-2"'
mailserver_1  | b'ip: "192.168.75.215"'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "app_id"'
mailserver_1  | b'  value: "85d139e7-9fb3-4041-b80a-5970f624a415"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "app_name"'
mailserver_1  | b'  value: "roster"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "instance_id"'
mailserver_1  | b'  value: "0"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "organization_id"'
mailserver_1  | b'  value: "fa94302b-462d-4e3d-9bc1-7a4af6025fdc"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "organization_name"'
mailserver_1  | b'  value: "welcome"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "process_id"'
mailserver_1  | b'  value: "85d139e7-9fb3-4041-b80a-5970f624a415"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "process_instance_id"'
mailserver_1  | b'  value: "9c890ccb-2268-45f8-400a-6a52"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "process_type"'
mailserver_1  | b'  value: "web"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "source_id"'
mailserver_1  | b'  value: "85d139e7-9fb3-4041-b80a-5970f624a415"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "space_id"'
mailserver_1  | b'  value: "67d9cef1-672d-4126-8969-905e0ad87ce2"'
mailserver_1  | b'}'
mailserver_1  | b'tags {'
mailserver_1  | b'  key: "space_name"'
mailserver_1  | b'  value: "dev"'
mailserver_1  | b'}'
mailserver_1  | ------------ END MESSAGE ------------
```