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
├── ldfi_interpreter
│   ├── __main__.py
│   ├── graphs
│   │   ├── TestHipsterShop.gv
│   │   ├── TestHipsterShop.gv.png
│   │   ├── TestHome.gv
│   │   └── TestHome.gv.png
│   ├── json_format.py
│   └── traces
│       ├── TestHipsterShop.json
│       └── TestHome.json
└── requirements.txt
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
    virtualenv --system-site-packages -p python3 ./venv
    source ./venv/bin/activate
```

#### 3.
Install `requirements.txt`
```
    cd ldfi-interpreter
    pip install -r requirements.txt
```

# Development Notes
### Hipster Shop DAG Notes
```
    Services

    client = client
    Frontend = 9f5a051c-a4a3-99bf-e5d0-250b0753c3a8
    ProductCatalogService = 5766d48d-ff75-30a4-54be-b4bcc59b6816"
    CurrencyService = 4d9f851b-5dbb-4343-8509-35de8ba20cca
    CartService =
    AdService = e02f6df3-c8df-4484-8004-ae2c43221017


    ListProductsRequest

```


## Data Structures Information
### Trace
Trace datastructure
```
Trace:
    id: int
    records: array of objects

```

### Record
Record datastructure
```
Record:
    message_name: string
    service: string
    timestamp: int
    type: int
    uuid: string

```
