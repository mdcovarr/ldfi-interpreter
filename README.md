# ldfi-interpreter
LDFI Integration with 3MileBeach

## Requirements
```
    python >= 3.9 (Although might work with older version, but not tested)
```

## Repo Structure
```
.
├── LICENSE
├── README.md
├── client
│   └── client.py
├── graphs
├── ldfi_interpreter
│   ├── __main__.py
│   └── json_format.py
├── requests
│   └── request-0.json
├── requirements.txt
└── traces
    └── trace-0.json
```
## Installation
#### 1.
In order to get `graphviz` to work on my Mac, I needed to install `graphviz` via Homebrew like so:
```
    brew install graphviz

    OR
    You need to make sure the Graphviz executables are on your systems' PATH
```

#### 2.
Setup a virtual env (Optional)
```
    cd ldfi-interpreter
    virtualenv --system-site-packages -p python3 ./venv
    source ./venv/bin/activate
```

#### 3.
Install `requirements.txt`
```
    cd ldfi-interpreter
    source ./venv/bin/activate
    pip install -r requirements.txt
```


# 3MileBeach Tracing and Fault Injection

## Client Request
```
    Request Data Strcture


    HTTPMethod:             int64
        HTTPGet             1
        HTTPPost            2


    ActionResponse:         int64
        PrintResponse:      1
        DeserializeTrace:   2
        CustomizedRspFunc:  3


    ExpectedResponse:       int64
        ContentType:        string
        Action:             ActionResponse



    Request:
        Method:             HTTPMethod
        URL:                string
        UrlValues:          url.Values // HTTP Post

        MessageName:        string
        Trace:              Trace
        Expect              ExpectResponse


    Requests:
        CookieUrl:          string
        Trace:              Trace

        Requests:           []Request

```
```
    Trace Data Structure


    Trace:
        Id:                 int64
        Records:            []*Records
        Rlfis:              []*Rlfis
        Tfis:               []*Tfis
```
```
    Record Data Structure


    MessageType:            int32
        Message_Request:    1
        Message_Response:   2

    RecordType              int32
        RecordSend:         1
        RecordReceive:      2

    Records
        Type:               RecordType
        Timestamp:          int64
        MessageName:        string
        Uuid:               string
        Service:            string
```
```
    Fault Data Structure


    FaultType:              int32
        FaultCrash:         1
        FaultDelay:         2

    TFIMeta:
        Name:               string
        Times:              int64
        Already:            int64

    TFI:
        Type:               FaultType
        Name:               []string
        Delay:              int64
        After:              []*TFIMeta
```
```
    Request Level Fault Injection Data Structure (Deleted)


    RLFI
        Type:               FaultType
        Name:               string
        Delay:              int64
```