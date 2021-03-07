# Cloud Foundry Application logs Alert

An email notification tool for Cloud Foundry applications. 

[![Codeship Status for kumbasar/cf-logs-alert](https://app.codeship.com/projects/3112835d-71ee-43c3-8a6d-7cdc27e3946e/status?branch=main)](https://app.codeship.com/projects/422129)
![cf-logs-alert](https://github.com/kumbasar/cf-logs-alert/workflows/cf-logs-alert/badge.svg)


## Usage

This tool posts email alerts for given a keyword list. To use the tool, first update the `config.json` file, according to your setup:

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

Now, you can execute the below command to start the tool:

```bash
chmod +x main.py
./main.py 
```

or

```bash
python main.py 
```

Also, you might build and run the tool in a Docker container. See provided `Dockerfile` as an example.

To build and run the tool via docker:

```bash
docker build -t cf-logger . 
docker run -t cf-logger   
```

## Proxy Configuration

You can set your proxy as follows:

```bash
export HTTPS_PROXY=<HTTPS_PROXY>
export HTTP_PROXY=<HTTP_PROXY>

./main.py
```

or

```bash
./main.py --proxy <HTTPS_PROXY>
```

##  Optional: Local email server for testing

Update `config.json` file as follows:

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

Execute the test email as follows:

```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```

Also, you can use `docker compose`:

In `config.json`, set `smtp` to `mailserver`. Example:

```JSON
[...]
    "smtp": "mailserver",
[...]
```

Execute below command:

```bash
docker-compose up --build
```