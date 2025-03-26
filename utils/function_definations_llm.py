function_definitions_objects_llm = {
    "vs_code_version": {
        "name": "vs_code_version",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {}
            },
            "required": []
        }
    },

    "make_http_requests_with_uv": {
        "name": "make_http_requests_with_uv",
        "description": "Extract the URL and query parameters from a question about making HTTP requests with UV, then perform the request and return results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query_params": {
                    "type": "object",
                    "description": "The query parameters to send with the request URL encoded parameters"
                },
                "url": {
                    "type": "string",
                    "description": "The URL to make the request to"
                }
            },
            "required": ["query_params","url"]
        }
    },

    "run_command_with_npx": {
        "name": "run_command_with_npx",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "use_google_sheets": {
        "name": "use_google_sheets",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "use_excel": {
        "name": "use_excel",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "use_devtools": {
        "name": "use_devtools",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

   "count_wednesdays": {
    "name": "count_wednesdays",
    "description": "Count the number of specific weekdays between two dates",
    "parameters": {
        "type": "object",
        "properties": {
            "start_date": {
                "type": "string",
                "description": "Start date in YYYY-MM-DD format"
            },
            "end_date": {
                "type": "string",
                "description": "End date in YYYY-MM-DD format"
            },
            "weekday": {
                "type": "integer",
                "description": "Day of week to count (0=Monday, 1=Tuesday, 2=Wednesday, etc.)"
            }
        },
        "required": ["start_date", "end_date"]
    }
},

    "extract_csv_from_a_zip": {
        "name": "extract_csv_from_a_zip",
        "description": "Extract a CSV file from a ZIP archive and return values from a specific column",
        "parameters": {
            "type": "object",
            "properties": {
                "zip_path": {
                    "type": "string",
                    "description": "Path to the ZIP file containing the CSV file"
                },
                "extract_to": {
                    "type": "string",
                    "description": "Directory to extract files to (default: 'extracted_files')"
                },
                "csv_filename": {
                    "type": "string",
                    "description": "Name of the CSV file to extract (default: 'extract.csv')"
                },
                "column_name": {
                    "type": "string",
                    "description": "Name of the column to extract values from (default: 'answer')"
                }
            },
            "required": ["zip_path"]
        }
    },

    "use_json": {
        "name": "use_json",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "input_data": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["input_data"]
        }
    },

    "multi_cursor_edits_to_convert_to_json": {
    "name": "multi_cursor_edits_to_convert_to_json",
    "description": "Converts a multi-line file containing key=value pairs into a JSON object",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file containing key=value pairs on separate lines"
            }
        },
        "required": ["file_path"]
        }
    },

    "css_selectors": {
        "name": "css_selectors",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "process_files_with_different_encodings": {
    "name": "process_files_with_different_encodings",
    "description": "Process files with different encodings and sum values associated with specific symbols",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the zip file containing files with different encodings (data1.csv in CP-1252, data2.csv in UTF-8, data3.txt in UTF-16)"
            }
        },
        "required": []
        }
    },

    "use_github": {
        "name": "use_github",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    "replace_across_files": {
    "name": "replace_across_files",
    "description": "Download and extract a zip file, replace 'IITM' (case-insensitive) with 'IIT Madras' in all files, and calculate a hash of the result",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the zip file containing the files to process"
            }
        },
        "required": ["file_path"]
    }
    },

    "list_files_and_attributes": {
    "name": "list_files_and_attributes",
    "description": "Download and extract a zip file, then list all files with their dates and sizes, calculating the total size of files meeting specific criteria",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the zip file containing the files to process"
            },
            "min_size": {
                "type": "integer",
                "description": "Minimum file size in bytes (default: 6262)"
            },
            "reference_date": {
                "type": "string",
                "description": "Reference date in format 'YYYY-MM-DD HH:MM:SS' (default: '2019-03-22 14:31:00')"
            },
            "timezone": {
                "type": "string",
                "description": "Timezone for reference date (default: 'Asia/Kolkata')"
            },
            "debug": {
                "type": "boolean",
                "description": "Whether to print debug information (default: False)"
            }
        },
        "required": ["file_path"]
    }
},

    "compare_files": {
    "name": "compare_files",
    "description": "Compare two files and analyze differences",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the zip file containing files to compare"
            }
        },
        "required": ["file_path"]
        }
    },

    "sql_ticket_sales": {
        "name": "sql_ticket_sales",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    "write_documentation_in_markdown": {
        "name": "write_documentation_in_markdown",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
# Completed
    "compress_an_image": {
        "name": "compress_an_image",
        "description": "Compress an image to be under 1,500 bytes and return it as base64",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file to compress"
                }
            },
            "required": ["image_path"]
        }
    },
# Completed
    "host_your_portfolio_on_github_pages": {
        "name": "host_your_portfolio_on_github_pages",
        "description": "Get the GitHub Pages URL for a specific user's portfolio",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The user's email address to look up their GitHub Pages URL"
                }
            },
            "required": ["email"]
        }
    },
# Completed
    "use_google_colab": {
        "name": "use_google_colab",
        "description": "Extract the email to get the result of running hashlib code in Google Colab",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address to use with Google Colab"
                }
            },
            "required": ["email"]
        }
    },
# Completed
    "use_an_image_library_in_google_colab": {
        "name": "use_an_image_library_in_google_colab",
        "description": "Process an image in Google Colab to count pixels with specific brightness",
        "parameters": {
            "type": "object",
            "properties": {
                "image_url": {
                    "type": "string",
                    "description": "URL of the image to process in Google Colab"
                }
            },
            "required": ["image_url"]
        }
    },

    "deploy_a_python_api_to_vercel": {
        "name": "deploy_a_python_api_to_vercel",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "create_a_github_action": {
        "name": "create_a_github_action",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "push_an_image_to_docker_hub": {
        "type": "function",
        "function": {
            "name": "push_an_image_to_docker_hub",
            "description": "Extracts parameters for Docker image creation and pushing to Docker Hub",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "The tag to be added to the Docker image(eg.'22ds3000103')"
                    }
                },
                "required": ["tag"]
            }
        }
    },

    "write_a_fastapi_server_to_serve_data": {
        "name": "write_a_fastapi_server_to_serve_data",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "run_a_local_llm_with_llamafile": {
        "name": "run_a_local_llm_with_llamafile",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "llm_sentiment_analysis": {
    "name": "llm_sentiment_analysis",
    "description": "Analyzes sentiment of text for DataSentinel Inc's internal monitoring dashboard, categorizing it as GOOD, BAD, or NEUTRAL.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
        }
    },

    "llm_token_cost": {
        "name": "llm_token_cost",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "generate_addresses_with_llms": {
        "name": "generate_addresses_with_llms",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    # Completed
    "llm_vision": {
    "name": "llm_vision",
    "description": "Generate a JSON body for an OpenAI vision API request.",
    "parameters": {
        "type": "object",
        "properties": {
            "model": {
                "type": "string",
                "description": "The OpenAI model to use for vision processing. Default is 'gpt-4o-mini'."
            },
            "messages": {
                "type": "array",
                "description": "User messages containing both text and an image URL.",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "string",
                            "enum": ["user"],
                            "description": "Role of the message sender."
                        },
                        "content": {
                            "type": "array",
                            "description": "Message content, including a text instruction and an image URL.",
                            "items": {
                                "oneOf": [
                                    {
                                        "type": "object",
                                        "properties": {
                                            "type": {"type": "string", "enum": ["text"]},
                                            "text": {"type": "string", "description": "Instruction for the model."}
                                        },
                                        "required": ["type", "text"]
                                    },
                                    {
                                        "type": "object",
                                        "properties": {
                                            "type": {"type": "string", "enum": ["image_url"]},
                                            "image_url": {
                                                "type": "object",
                                                "properties": {
                                                    "url": {"type": "string", "description": "URL of the image."}
                                                },
                                                "required": ["url"]
                                            }
                                        },
                                        "required": ["type", "image_url"]
                                    }
                                ]
                            }
                        }
                    },
                    "required": ["role", "content"]
                }
            }
        },
        "required": ["model", "messages"]
    }
    },

    # Completed
        "llm_embeddings" : {
    "name": "llm_embeddings",
    "description": "Generate a JSON body for an OpenAI embeddings API request using the text-embedding-3-small model.",
    "parameters": {
        "type": "object",
        "properties": {
            "model": {"type": "string", "enum": ["text-embedding-3-small"], "description": "The OpenAI model to use for generating text embeddings."},
            "input_texts": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of text strings to generate embeddings for."
            }
        },
        "required": ["model", "input_texts"]
        }
    },

    # Completed
    "embedding_similarity": {
        "name": "embedding_similarity",
        "description": "Calculate cosine similarity between embeddings and return the most similar pair.",
        "parameters": {
            "type": "object",
            "properties": {}
            },
            "required": []
        },

    "vector_databases": {
        "name": "vector_databases",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "function_calling": {
        "name": "function_calling",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "get_an_llm_to_say_yes": {
        "name": "get_an_llm_to_say_yes",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "import_html_to_google_sheets": {
        "name": "import_html_to_google_sheets",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "scrape_imdb_movies": {
        "name": "fetch_filtered_imdb_titles",
        "description": "Fetches movie titles from IMDb within a specified rating range",
        "parameters": {
            "type": "object",
            "properties": {
                "min_rating": {
                    "type": "number",
                    "description": "Minimum IMDb rating (0-10)"
                },
                "max_rating": {
                    "type": "number",
                    "description": "Maximum IMDb rating (0-10)"
                }
            },
            "required": ["min_rating", "max_rating"]
        }
    },

    "wikipedia_outline": {
        "name": "wikipedia_outline",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "scrape_the_bbc_weather_api": {
    "type": "function",
    "function": {
        "name": "scrape_the_bbc_weather_api",
        "description": "Fetches and scrapes weather forecast data for a specified city from the BBC Weather API and website, returning a JSON object mapping dates to weather descriptions.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city for which to retrieve the weather forecast (e.g., 'Luanda', 'London')."
                }
            },
            "required": ["city"]
        }
    }
},

    "find_the_bounding_box_of_a_city": {
    "type": "function",
    "function": {
        "name": "find_the_bounding_box_of_a_city",
        "description": "Fetches the minimum latitude of the bounding box for a specified city in a country using the Nominatim API, optionally filtering by an osm_id ending pattern to disambiguate multiple entries.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to retrieve geospatial data for (e.g., 'Tianjin')."
                },
                "country": {
                    "type": "string",
                    "description": "The name of the country where the city is located (e.g., 'China')."
                },
                "osm_id_ending": {
                    "type": "string",
                    "description": "The ending pattern of the osm_id to filter the correct city instance (e.g., '2077'). Optional; if omitted, returns the first match."
                }
            },
            "required": ["city", "country"]
        }
    }
},

    "search_hacker_news": {
    "type": "function",
    "function": {
        "name": "search_hacker_news",
        "description": "Searches Hacker News via the HNRSS API for the latest post mentioning a specified technology topic with a minimum number of points, returning the post's link as a JSON object.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The technology topic to search for in Hacker News posts (e.g., 'python', 'blockchain')."
                },
                "points": {
                    "type": "integer",
                    "description": "The minimum number of points the post must have to be considered relevant."
                }
            },
            "required": ["query", "points"]
        }
    }
},

    "find_newest_github_user": {
    "type": "function",
    "function": {
        "name": "find_newest_github_user",
        "description": "Searches GitHub for the newest user in a specified location with a follower count based on a comparison operator, excluding users who joined after March 23, 2025, 3:57:03 PM PDT. Returns the creation date in ISO 8601 format.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city to search for GitHub users (e.g., 'Delhi')."
                },
                "followers": {
                    "type": "integer",
                    "description": "The number of followers to filter by."
                },
                "operator": {
                    "type": "string",
                    "enum": ["gt", "lt", "eq"],
                    "description": "The comparison operator for followers: 'gt' for greater than, 'lt' for less than, 'eq' for equal to."
                }
            },
            "required": ["location", "followers", "operator"]
        }
    }
},

    "create_a_scheduled_github_action": {
        "name": "create_a_scheduled_github_action",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "extract_tables_from_pdf": {
        "name": "extract_tables_from_pdf",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "convert_a_pdf_to_markdown": {
        "name": "convert_a_pdf_to_markdown",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "clean_up_excel_sales_data": {
        "name": "clean_up_excel_sales_data",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "clean_up_student_marks": {
        "type": "function",
        "function": {
            "name": "clean_up_student_marks",
            "description": "Analyzes logs to count the number of successful GET requests matching criteria such as URL prefix, weekday, time window, month, and year.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the gzipped log file."
                    },
                    "section_prefix": {
                        "type": "string",
                        "description": "URL prefix to filter log entries (e.g., '/telugu/')."
                    },
                    "weekday": {
                        "type": "integer",
                        "description": "Day of the week as an integer (0=Monday, ..., 6=Sunday)."
                    },
                    "start_hour": {
                        "type": "integer",
                        "description": "Start hour (inclusive) in 24-hour format."
                    },
                    "end_hour": {
                        "type": "integer",
                        "description": "End hour (exclusive) in 24-hour format."
                    },
                    "month": {
                        "type": "integer",
                        "description": "Month number (e.g., 5 for May)."
                    },
                    "year": {
                        "type": "integer",
                        "description": "Year (e.g., 2024)."
                    }
                },
                "required": [
                    "file_path",
                    "section_prefix",
                    "weekday",
                    "start_hour",
                    "end_hour",
                    "month",
                    "year"
                ]
            }
        }
    },
"apache_log_requests": {
    "name": "apache_log_requests",
    "description": "Extracts and analyzes Apache log requests for specific conditions, such as peak usage periods, request types, and success criteria.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The file path of the GZipped Apache log file."
            },
            "topic_heading": {
                "type": "string",
                "description": "A short heading summarizing the analysis topic."
            },
            "start_time": {
                "type": "string",
                "description": "The start time of the time window for analysis, in HH format (24-hour)."
            },
            "end_time": {
                "type": "string",
                "description": "The end time (exclusive) of the time window for analysis, in HH format (24-hour)."
            },
            "day": {
                "type": "string",
                "description": "The specific day for analysis (e.g., 'Sunday')."
            }
        },
        "required": ["file_path", "topic_heading", "start_time", "end_time", "day"]
    }
}
,

"apache_log_downloads": {
    "name": "apache_log_downloads",
    "description": "Analyzes an Apache log file to track bandwidth usage for a specific station and date. The function filters log entries based on a given date and extracts only those requests related to a specific station. It then aggregates data by IP address, calculating the total bytes downloaded per IP. Finally, it identifies the top data-consuming IP and reports the total bytes downloaded by that IP.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The full file path of the Apache log file (GZipped format)."
            },
            "station_name": {
                "type": "string",
                "description": "The name of the station or content category being analyzed (e.g., 'tamilmp3')."
            },
            "date": {
                "type": "string",
                "format": "date",
                "description": "The specific date (YYYY-MM-DD) for which log entries should be filtered."
            }
        },
        "required": ["file_path", "station_name", "date"]
    }
}
,

    "clean_up_sales_data": {
        "name": "clean_up_sales_data",
        "description": "Clean up the sales data given in the json file. To do this, find the product, city and minimum units (min_units) asked for in the question",
        "parameters": {
            "type": "object",
            "properties": {
                  "file_path": {
                    "type": "string",
                    "description": "The JSON file containing product data."
                },
                "product": {
                    "type": "string",
                    "description": "The product for which we want to find the number of units sold in a given city and minimum order quantity per transaction"
                },
                "city": {
                    "type": "string",
                    "description": "The city for which we want to find the number of units sold in a given product and minimum order quantity per transaction"
                },
                "min_units": {
                    "type": "number",
                    "description": "The minimum units of the product per transaction for which we want to find the number of units sold in a given city."
                }
              
            },
            "required": [ "file_path","product", "city", "min_units"]
        }
    },
    

    "parse_partial_json": {
        "name": "parse_partial_json",
        "description": "Sum up the values of the sales field in the jsonl file",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description":"Path to the jsonl file from which we will sum the values contained in sales field"
                }
            },
            "required": ["file_path"]
        }
    },

    "extract_nested_json_keys": {
        "name": "extract_nested_json_keys",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

"duckdb_social_media_interactions": {
    "name": "duckdb_social_media_interactions",
    "description": "description",
    "parameters": {
        "type": "object",
        "properties": {
            "start_time": {
                "type": "string",
                "description": "The time after which to find all post IDs in the DuckDB query"
            },
            "number_of_stars": {
                "type": "integer",
                "description": "The minimum number of useful stars needed in the DuckDB query"
            },
            "number_of_comments": {
                "type": "integer",
                "description": "The minimum number of useful comments needed in the DuckDB query"
            }
        },
        "required": ["start_time", "number_of_stars", "number_of_comments"]
    }
}
,

    "transcribe_a_youtube_video": {
        "name": "transcribe_a_youtube_video",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },

    "reconstruct_an_image": {
        "name": "reconstruct_an_image",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract the data from"
                }
            },
            "required": ["text"]
        }
    },
}
