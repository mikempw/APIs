[openapi_schema.json](https://github.com/user-attachments/files/16830707/openapi_schema.json)# APIs
Discovering APIs via syslog, through an iRule. Parsing the data to generate OpenAPI 3.0 and data visualization

Place the Telemetry iRule on the BIG-IP

Create a pool on the BIG-IP that references separate syslog servers we will be sending traffic to
  Ensure this location is a server that will just receive this traffic - please don't intermingle regular syslog traffic with this collector

Add the iRule to all Virtual Servers you want to capture web traffic 

As per the iRule instructions
    ###User-Edit Variables start###
    set z1_http_content_type logging-pool ; #Name of LTM pool to use for receiving this data
    set z1_remoteLogProtocol UDP ; #UDP or TCP
    set z1_globalStringLimit 100 ; #How many characters to collect from user-supplied HTTP values like HTTP host, version, referrer. 
    set z1_uriStringLimit 600 ; #How many characters to collect from HTTP value of URI
    ###User-Edit Variables end###

To generate an OpenAPI schema
  Run the syslog-to-openapi.py on a syslog.log file
    Example: syslog-to-openapi.py syslog.log

To generate a .CSV file
  Run the syslog-to-csv.py on a syslog.log file - this will generate a f5_api_data.csv
  Example: syslog-to-csv.py syslog.log

Example syslog.log to f5_api_data.csv output:
timestamp	http_uri	http_host	http_method	http_status	virtual_server	pool	http_referrer	http_content_type	http_user_agent	http_version	vip
9/1/2024 0:00	/f5_waf_tester/?f5_waf_tester_parameter=AND+SELECT+SUBSTRING%28column_name%2C1%2C1%29+FROM+information_schema.columns+%3E+%27A%27	10.1.10.20	GET	404	/Common/west-app-vs20	/Common/php_pool 10.1.20.12 80			python-requests/2.25.1	1.1	10.1.10.20
9/1/2024 0:00	/f5_waf_tester/	10.1.10.20	GET	404	/Common/west-app-vs20	/Common/php_pool 10.1.20.12 80			f5_waf_tester 0.1.1b	1.1	10.1.10.20
9/1/2024 0:00	/../../etc/passwd	10.1.10.20	GET	400	/Common/west-app-vs20	/Common/php_pool 10.1.20.12 80			f5_waf_tester 0.1.1b	1.1	10.1.10.20
9/1/2024 0:00	/f5_waf_tester/?f5_waf_tester_parameter=%2526%2520powershell-WindowStyle%2520Hidden%2520-encode	10.1.10.20	GET	404	/Common/west-app-vs20	/Common/php_pool 10.1.20.12 80			f5_waf_tester 0.1.1b	1.1	10.1.10.20
9/1/2024 0:00	/f5_waf_tester/%7B%24where%3A+function%28%29+%7B+return+db.getCollectionNames%28%29%3B+%7D%7D	10.1.10.30	GET	404	/Common/west-app-vs30	/Common/image_pool 10.1.20.15 80			f5_waf_tester 0.1.1b	1.1	10.1.10.30
9/1/2024 0:01	/f5_waf_tester/?f5_waf_tester_parameter=or+1%3D1+--	10.1.10.30	GET	404	/Common/west-app-vs30	/Common/image_pool 10.1.20.15 80			f5_waf_tester 0.1.1b	1.1	10.1.10.30
9/1/2024 0:01	/f5_waf_tester/?f5_waf_tester_parameter=O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D	10.1.10.30	GET	404	/Common/west-app-vs30	/Common/image_pool 10.1.20.15 80			f5_waf_tester 0.1.1b	1.1	10.1.10.30

To generate an overview of APIs, Status Code etc..
  Run the api-summary-generator.py on the f5_api_data.csv file created above
  Example: api-summary-generator.py f5_api_data.csv

Example OpenAPI schema output:
  [Uploading openapi_s{
  "openapi": "3.0.0",
  "info": {
    "title": "Discovered API from F5 Syslog",
    "version": "1.0.0",
    "description": "API discovered from F5 syslog messages"
  },
  "paths": {
    "/f5_waf_tester/?f5_waf_tester_parameter=AND+SELECT+SUBSTRING%28column_name%2C1%2C1%29+FROM+information_schema.columns+%3E+%27A%27": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=AND+SELECT+SUBSTRING%28column_name%2C1%2C1%29+FROM+information_schema.columns+%3E+%27A%27",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/?f5_waf_tester_parameter=AND+SELECT+SUBSTRING%28column_name%2C1%2C1%29+FROM+information_schema.columns+%3E+%27A%27",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml"
        ],
        "x-pools": [
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/": {
      "get": {
        "summary": "GET request to /f5_waf_tester/",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "408": {
            "description": "Client error (Status: 408)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "trace": {
        "summary": "TRACE request to /f5_waf_tester/",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/../../etc/passwd": {
      "get": {
        "summary": "GET request to /../../etc/passwd",
        "responses": {
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=%2526%2520powershell-WindowStyle%2520Hidden%2520-encode": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=%2526%2520powershell-WindowStyle%2520Hidden%2520-encode",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/%7B%24where%3A+function%28%29+%7B+return+db.getCollectionNames%28%29%3B+%7D%7D": {
      "get": {
        "summary": "GET request to /f5_waf_tester/%7B%24where%3A+function%28%29+%7B+return+db.getCollectionNames%28%29%3B+%7D%7D",
        "responses": {
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=or+1%3D1+--": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=or+1%3D1+--",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D",
        "responses": {
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/?f5_waf_tester_parameter=O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/image_pool 10.1.20.15 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "trace": {
        "summary": "TRACE request to /f5_waf_tester/?f5_waf_tester_parameter=O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.11 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=%3Cscript%3Evar+a+%3D+1%3B%3C%2Fscript%3E": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=%3Cscript%3Evar+a+%3D+1%3B%3C%2Fscript%3E",
        "responses": {
          "408": {
            "description": "Client error (Status: 408)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/backup/": {
      "get": {
        "summary": "GET request to /backup/",
        "responses": {
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D": {
      "get": {
        "summary": "GET request to /f5_waf_tester/O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D",
        "responses": {
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/O%3A6%3A%22+attack+%22%3A3%3A%7Bs%3A4%3A%22+file+%22%3Bs%3A9%3A%22+shell.php+%22%3Bs%3A4%3A%22+data+%22%3Bs%3A19%3A%22+%3C++%3F+php+phpinfo%28%29%3B%3F++%3E+%22%3B%7D",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/or%091%3D1%09--": {
      "get": {
        "summary": "GET request to /f5_waf_tester/or%091%3D1%09--",
        "responses": {
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/": {
      "get": {
        "summary": "GET request to /",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "408": {
            "description": "Client error (Status: 408)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "trace": {
        "summary": "TRACE request to /",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=exploit.php%00.jpg": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=exploit.php%00.jpg",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "trace": {
        "summary": "TRACE request to /f5_waf_tester/?f5_waf_tester_parameter=exploit.php%00.jpg",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=%27+onmouseover%3D%27var+a%3D1%3B": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=%27+onmouseover%3D%27var+a%3D1%3B",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/test.aspx%3A%3A%24DATA": {
      "get": {
        "summary": "GET request to /f5_waf_tester/test.aspx%3A%3A%24DATA",
        "responses": {
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/test.aspx%3A%3A%24DATA",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/image_pool 10.1.20.15 80"
        ]
      },
      "trace": {
        "summary": "TRACE request to /f5_waf_tester/test.aspx%3A%3A%24DATA",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/image_pool 10.1.20.15 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=..%2F..%2Fetc%2Fpasswd": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=..%2F..%2Fetc%2Fpasswd",
        "responses": {
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/?f5_waf_tester_parameter=..%2F..%2Fetc%2Fpasswd",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=9999999+UNION+SELECT+1%2C2": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=9999999+UNION+SELECT+1%2C2",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/?f5_waf_tester_parameter=9999999+UNION+SELECT+1%2C2",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/AND+SELECT+SUBSTRING%28column_name%2C1%2C1%29+FROM+information_schema.columns+%3E+%27A%27": {
      "get": {
        "summary": "GET request to /f5_waf_tester/AND+SELECT+SUBSTRING%28column_name%2C1%2C1%29+FROM+information_schema.columns+%3E+%27A%27",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=%7B%24where%3A+function%28%29+%7B+return+db.getCollectionNames%28%29%3B+%7D%7D": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=%7B%24where%3A+function%28%29+%7B+return+db.getCollectionNames%28%29%3B+%7D%7D",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/x%3Deval%3Bx%281%29": {
      "get": {
        "summary": "GET request to /f5_waf_tester/x%3Deval%3Bx%281%29",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/%2526%2520powershell-WindowStyle%2520Hidden%2520-encode": {
      "get": {
        "summary": "GET request to /f5_waf_tester/%2526%2520powershell-WindowStyle%2520Hidden%2520-encode",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=x%3Deval%3Bx%281%29": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=x%3Deval%3Bx%281%29",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/%26+uname": {
      "get": {
        "summary": "GET request to /f5_waf_tester/%26+uname",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/%27+onmouseover%3D%27var+a%3D1%3B": {
      "get": {
        "summary": "GET request to /f5_waf_tester/%27+onmouseover%3D%27var+a%3D1%3B",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml",
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/_%24%24ND_FUNC%24%24_function+%28%29%7Brequire%28%27child_process%27%29.exec%28%27ls+/%27%2C+function%28error%2C+stdout%2C+stderr%29+%7B+console.log%28stdout%29+%7D%29%3B%7D%28%29": {
      "get": {
        "summary": "GET request to /f5_waf_tester/_%24%24ND_FUNC%24%24_function+%28%29%7Brequire%28%27child_process%27%29.exec%28%27ls+/%27%2C+function%28error%2C+stdout%2C+stderr%29+%7B+console.log%28stdout%29+%7D%29%3B%7D%28%29",
        "responses": {
          "400": {
            "description": "Client error (Status: 400)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/xml"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "post": {
        "summary": "POST request to /f5_waf_tester/_%24%24ND_FUNC%24%24_function+%28%29%7Brequire%28%27child_process%27%29.exec%28%27ls+/%27%2C+function%28error%2C+stdout%2C+stderr%29+%7B+console.log%28stdout%29+%7D%29%3B%7D%28%29",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=%26+uname": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=%26+uname",
        "responses": {
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/%3Cscript%3Evar+a+%3D+1%3B%3C/script%3E": {
      "get": {
        "summary": "GET request to /f5_waf_tester/%3Cscript%3Evar+a+%3D+1%3B%3C/script%3E",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      },
      "trace": {
        "summary": "TRACE request to /f5_waf_tester/%3Cscript%3Evar+a+%3D+1%3B%3C/script%3E",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.11 80"
        ]
      }
    },
    "/f5_waf_tester/9999999+UNION+SELECT+1%2C2": {
      "get": {
        "summary": "GET request to /f5_waf_tester/9999999+UNION+SELECT+1%2C2",
        "responses": {
          "0": {
            "description": "Unknown status (Status: 0)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/f5_waf_tester/?f5_waf_tester_parameter=_%24%24ND_FUNC%24%24_function+%28%29%7Brequire%28%27child_process%27%29.exec%28%27ls+%2F%27%2C+function%28error%2C+stdout%2C+stderr%29+%7B+console.log%28stdout%29+%7D%29%3B%7D%28%29": {
      "get": {
        "summary": "GET request to /f5_waf_tester/?f5_waf_tester_parameter=_%24%24ND_FUNC%24%24_function+%28%29%7Brequire%28%27child_process%27%29.exec%28%27ls+%2F%27%2C+function%28error%2C+stdout%2C+stderr%29+%7B+console.log%28stdout%29+%7D%29%3B%7D%28%29",
        "responses": {
          "404": {
            "description": "Client error (Status: 404)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [
          "application/json"
        ],
        "x-pools": [
          "/Common/php_pool 10.1.20.12 80",
          "/Common/image_pool 10.1.20.15 80",
          "/Common/php_pool 10.1.20.11 80",
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    },
    "/images/f5logo.gif": {
      "get": {
        "summary": "GET request to /images/f5logo.gif",
        "responses": {
          "200": {
            "description": "Successful response (Status: 200)",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "x-content-types": [],
        "x-pools": [
          "/Common/image_pool 10.1.20.14 80"
        ]
      }
    }
  }
}chema.json…]()
