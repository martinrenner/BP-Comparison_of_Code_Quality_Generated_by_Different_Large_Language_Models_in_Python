# Constants for the convertor_to_csv module

# RESULTS_DIR - the directory where the results will be stored
RESULTS_DIR = "results"

# CHALLENGES - list of challenges used in scraper
CHALLENGES = {
    "calculator": {
        "regex_rules": [
            {
                "file": "1_code_compilability-{model}.txt",
                "columns": ["code_compilability"],
                "regex": [
                    {
                        "type": "bool",
                        "rule": r"Yes, the code is compilable."
                    }
                ],
            },
            {
                "file": "2_code_length-{model}.txt",
                "columns": ["code_length"],
                "regex": [
                    {
                        "type": "int",
                        "rule": r"Number of lines: (\d+)"
                    }
                ],
            },
            {
                "file": "3_modularity-{model}.txt",
                "columns": ["modularity-number_of_classes", "modularity-number_of_methods", "modularity-number_of_functions"],
                "regex": [
                    {
                        "type": "int",
                        "rule":  r"Number of classes: (\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Number of methods: (\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Number of functions: (\d+)"
                    }
                ],
            },
            {
                "file": "4_functional_completeness-{model}.txt",
                "columns": ["functional_completeness"],
                "regex": [
                    {
                        "type": "bool",
                        "rule": r"All classes and methods exist and have the correct parameters."
                    }
                ],
            },
            {
                "file": "5_functional_correctness-{model}.txt",
                "columns": ["functional_correctness-fail", "functional_correctness-pass"],
                "regex": [
                    {
                        "type": "int",
                        "rule": r"(\d+) failed", 
                        
                    },
                    {
                        "type": "int",
                        "rule": r"(\d+) passed"
                    }
                ],
            },
            {
                "file": "6_time_behaviour-{model}.txt", 
                "columns": [ "time_behaviour-calculate_add", "time_behaviour-calculate_subtract", "time_behaviour-calculate_multiply", "time_behaviour-calculate_divide", "time_behaviour-calculate_composite"],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Average time for calculate \(1974349\+7972327\): (\d+).(\d+) seconds\n",
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for calculate \(1974349\-7972327\): (\d+).(\d+) seconds\n",
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for calculate \(1974349\*7972327\): (\d+).(\d+) seconds\n",
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for calculate \(1974349\/7972327\): (\d+).(\d+) seconds\n",
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for calculate \(1974349\+7972327\-1974349\*7972327\/964\): (\d+).(\d+) seconds\n",
                    }
                ],
            },
            {
                "file": "7_performance_efficiency-CPU-{model}.txt",
                "columns": [
                    "performance_efficiency-CPU-calculate_add-user_time",
                    "performance_efficiency-CPU-calculate_add-system_time",
                    "performance_efficiency-CPU-calculate_subtract-user_time",
                    "performance_efficiency-CPU-calculate_subtract-system_time",
                    "performance_efficiency-CPU-calculate_multiply-user_time",
                    "performance_efficiency-CPU-calculate_multiply-system_time",
                    "performance_efficiency-CPU-calculate_divide-user_time",
                    "performance_efficiency-CPU-calculate_divide-system_time",
                    "performance_efficiency-CPU-calculate_composite-user_time",
                    "performance_efficiency-CPU-calculate_composite-system_time",
                ],
                "regex": [
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - calculate \(1974349\+7972327\): User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - calculate \(1974349\-7972327\): User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - calculate \(1974349\*7972327\): User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - calculate \(1974349\/7972327\): User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - calculate \(1974349\+7972327\-1974349\*7972327\/964\): User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    }
                ],
            },
            {
                "file": "8_performance_efficiency-RAM-{model}.txt",
                "columns": [
                    "performance_efficiency-RAM-calculate_add",
                    "performance_efficiency-RAM-calculate_subtract",
                    "performance_efficiency-RAM-calculate_multiply",
                    "performance_efficiency-RAM-calculate_divide",
                    "performance_efficiency-RAM-calculate_composite",
                ],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Memory deltas for calculate \(1974349\+7972327\): (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for calculate \(1974349\-7972327\): (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for calculate \(1974349\*7972327\): (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for calculate \(1974349\/7972327\): (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for calculate \(1974349\+7972327\-1974349\*7972327\/964\): (-?\d+).(\d+) MB",
                    }
                ],
            },
            {
                "file": "9_analysibility-{model}.txt",
                "columns": ["analysability-score", "analysability-max_score"],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Your code has been rated at (\d+).(\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Your code has been rated at \d+.\d+/(\d+)"
                    }
                ]
                    
            },
        ]
    },
    "todo_list": {
        "regex_rules": [
            {
                "file": "1_code_compilability-{model}.txt",
                "columns": ["code_compilability"],
                "regex": [
                    {
                        "type": "bool",
                        "rule": r"Yes, the code is compilable."
                    }
                ],
            },
            {
                "file": "2_code_length-{model}.txt",
                "columns": ["code_length"],
                "regex": [
                    {
                        "type": "int",
                        "rule": r"Number of lines: (\d+)"
                    }
                ],
            },
            {
                "file": "3_modularity-{model}.txt",
                "columns": ["modularity-number_of_classes", "modularity-number_of_methods", "modularity-number_of_functions"],
                "regex": [
                    {
                        "type": "int",
                        "rule":  r"Number of classes: (\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Number of methods: (\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Number of functions: (\d+)"
                    }
                ],
            },
            {
                "file": "4_functional_completeness-{model}.txt",
                "columns": ["functional_completeness"],
                "regex": [
                    {
                        "type": "bool",
                        "rule": r"All classes and methods exist and have the correct parameters."
                    }
                ],
            },
            {
                "file": "5_functional_correctness-{model}.txt",
                "columns": ["functional_correctness-fail", "functional_correctness-pass"],
                "regex": [
                    {
                        "type": "int",
                        "rule": r"(\d+) failed", 
                        
                    },
                    {
                        "type": "int",
                        "rule": r"(\d+) passed"
                    }
                ],
            },
            {
                "file": "6_time_behaviour-{model}.txt",
                "columns": ["time_behaviour-add_task", "time_behaviour-get_all_tasks", "time_behaviour-search_task-by_name", "time_behaviour-search_task-by_description", "time_behaviour-finish_task", "time_behaviour-remove_task"],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Average time for add: (\d+).(\d+) seconds"
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for get_all: (\d+).(\d+) seconds"
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 2,
                        "expected_columns": 2,
                        "rule": r"Average time for search: (\d+).(\d+) seconds"
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for finish: (\d+).(\d+) seconds"
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for remove: (\d+).(\d+) seconds"
                    }
                ],
            },
            {
                "file": "7_performance_efficiency-CPU-{model}.txt",
                "columns": ["performance_efficiency-CPU-add_task-user_time", "performance_efficiency-CPU-add_task-system_time", "performance_efficiency-CPU-get_all_tasks-user_time", "performance_efficiency-CPU-get_all_tasks-system_time", "performance_efficiency-CPU-search_task-by_name-user_time", "performance_efficiency-CPU-search_task-by_name-system_time", "performance_efficiency-CPU-search_task-by_description-user_time", "performance_efficiency-CPU-search_task-by_description-system_time", "performance_efficiency-CPU-finish_task-user_time",  "performance_efficiency-CPU-finish_task-system_time", "performance_efficiency-CPU-remove_task-user_time", "performance_efficiency-CPU-remove_task-system_time"],
                "regex": [
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - add: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - get_all: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 2,
                        "expected_columns": 4,
                        "rule": r"CPU time - search: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n"
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - finish: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - remove: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    }
                ],
            },
            {
                "file": "8_performance_efficiency-RAM-{model}.txt",
                "columns": ["performance_efficiency-RAM-add_task", "performance_efficiency-RAM-get_all_tasks", "performance_efficiency-RAM-search_task", "performance_efficiency-RAM-search_task-by_name", "performance_efficiency-RAM-search_task-by_description", "performance_efficiency-RAM-remove_task"],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Memory deltas for add: (-?\d+).(\d+) MB"
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for get_all: (-?\d+).(\d+) MB"
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 2,
                        "expected_columns": 2,
                        "rule": r"Memory deltas for search: (-?\d+).(\d+) MB"
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for finish: (-?\d+).(\d+) MB"
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for remove: (-?\d+).(\d+) MB"
                    }
                ],
            },
            {
                "file": "9_analysibility-{model}.txt",
                "columns": ["analysability-score", "analysability-max_score"],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Your code has been rated at (\d+).(\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Your code has been rated at \d+.\d+/(\d+)"
                    }
                ]
                    
            },
        ]
    },
    "ascii_art": {
        "regex_rules": [
            {
                "file": "1_code_compilability-{model}.txt",
                "columns": ["code_compilability"],
                "regex": [
                    {
                        "type": "bool",
                        "rule": r"Yes, the code is compilable."
                    }
                ],
            },
            {
                "file": "2_code_length-{model}.txt",
                "columns": ["code_length"],
                "regex": [
                    {
                        "type": "int",
                        "rule": r"Number of lines: (\d+)"
                    }
                ],
            },
            {
                "file": "3_modularity-{model}.txt",
                "columns": ["modularity-number_of_classes", "modularity-number_of_methods", "modularity-number_of_functions"],
                "regex": [
                    {
                        "type": "int",
                        "rule":  r"Number of classes: (\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Number of methods: (\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Number of functions: (\d+)"
                    }
                ],
            },
            {
                "file": "4_functional_completeness-{model}.txt",
                "columns": ["functional_completeness"],
                "regex": [
                    {
                        "type": "bool",
                        "rule": r"All classes and methods exist and have the correct parameters."
                    }
                ],
            },
            {
                "file": "5_functional_correctness-{model}.txt",
                "columns": ["functional_correctness-fail", "functional_correctness-pass"],
                "regex": [
                    {
                        "type": "int",
                        "rule": r"(\d+) failed", 
                        
                    },
                    {
                        "type": "int",
                        "rule": r"(\d+) passed"
                    }
                ],
            },
            {
                "file": "6_time_behaviour-{model}.txt", 
                "columns": [
                    "time_behaviour-draw_square",
                    "time_behaviour-draw_rectangle",
                    "time_behaviour-draw_parallelogram",
                    "time_behaviour-draw_triangle",
                    "time_behaviour-draw_pyramid",    
                ],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Average time for draw_square: (\d+).(\d+) seconds\n"
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for draw_rectangle: (\d+).(\d+) seconds\n"
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for draw_parallelogram: (\d+).(\d+) seconds\n"
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for draw_triangle: (\d+).(\d+) seconds\n"
                    },
                    {
                        "type": "float",
                        "rule": r"Average time for draw_pyramid: (\d+).(\d+) seconds\n"
                    }
                ],
            },
            {
                "file": "7_performance_efficiency-CPU-{model}.txt",
                "columns": [
                    "performance_efficiency-CPU-draw_square-user_time",
                    "performance_efficiency-CPU-draw_square-system_time",
                    "performance_efficiency-CPU-draw_rectangle-user_time",
                    "performance_efficiency-CPU-draw_rectangle-system_time",
                    "performance_efficiency-CPU-draw_parallelogram-user_time",
                    "performance_efficiency-CPU-draw_parallelogram-system_time",
                    "performance_efficiency-CPU-draw_triangle-user_time",
                    "performance_efficiency-CPU-draw_triangle-system_time",
                    "performance_efficiency-CPU-draw_pyramid-user_time",
                    "performance_efficiency-CPU-draw_pyramid-system_time",
                ],
                "regex": [
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - draw_square: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - draw_rectangle: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - draw_parallelogram: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - draw_triangle: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    },
                    {
                        "type": "float_multiple",
                        "expected_rows": 1,
                        "expected_columns": 4,
                        "rule": r"CPU time - draw_pyramid: User time = (\d+).(\d+)s, System time = (\d+).(\d+)s\n",
                    }
                ],
            },
            {
                "file": "8_performance_efficiency-RAM-{model}.txt",
                "columns": [
                    "performance_efficiency-RAM-draw_square",
                    "performance_efficiency-RAM-draw_rectangle",
                    "performance_efficiency-RAM-draw_parallelogram",
                    "performance_efficiency-RAM-draw_triangle",
                    "performance_efficiency-RAM-draw_pyramid",
                ],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Memory deltas for draw_square: (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for draw_rectangle: (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for draw_parallelogram: (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for draw_triangle: (-?\d+).(\d+) MB",
                    },
                    {
                        "type": "float",
                        "rule": r"Memory deltas for draw_pyramid: (-?\d+).(\d+) MB",
                    }
                ],
            },
            {
                "file": "9_analysibility-{model}.txt",
                "columns": ["analysability-score", "analysability-max_score"],
                "regex": [
                    {
                        "type": "float",
                        "rule": r"Your code has been rated at (\d+).(\d+)"
                    },
                    {
                        "type": "int",
                        "rule": r"Your code has been rated at \d+.\d+/(\d+)"
                    }
                ]
                    
            },
        ]
    },
}

# PROMPTS - list of prompts used in scraper
PROMPTS = [
    "1-zero_shot",
    "2-few_shot",
    "3-chain_of_thoughts-zero_shot",
    "4-chain_of_thoughts-few_shot",
    "5-role-zero_shot",
    "6-role-few_shot",
]

# MODELS - list of models used in scraper
MODELS = ["chatgpt", "claude", "gemini"]

# MODEL_DETAILS - dictionary with model details (added to the results csv)
MODEL_DETAILS = {
    "chatgpt": {"provider": "OpenAI", "model": "o3-mini-high"},
    "claude": {"provider": "Anthropic", "model": "Claude 3.7 Sonnet"},
    "gemini": {"provider": "Google", "model": "Gemini 2.0 Pro Experimental"},
}

# ITERATIONS - number of iterations used in scraper
ITERATIONS = 10
