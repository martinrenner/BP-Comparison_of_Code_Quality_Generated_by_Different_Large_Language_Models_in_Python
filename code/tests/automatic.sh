#!/usr/bin/env bash
# Run: ./code/tests/automatic.sh                                                                                                                                # Run all the tests

# CONFIG FOLDERS
TESTS_FOLDER="code/tests"                                                                                                                                       # Default folder with tests
GENERATED_FOLDER="generated/code"                                                                                                                               # Default folder with generated python files
RESULTS_FOLDER="results"                                                                                                                                        # Results folder

# CONFIG TESTS
TESTS=("1_code_compilability" "4_functional_completeness" "6_time_behaviour" "7_performance_efficiency-CPU" "8_performance_efficiency-RAM" "9_analysibility") # List of tests to run
PYTESTS=("5_functional_correctness-chatgpt" "5_functional_correctness-claude" "5_functional_correctness-gemini")                                                # List of pytest tests to run
ALLTESTS=("${TESTS[@]}" "${PYTESTS[@]}")                                                                                                                        # List of all tests to run

# CONFIG
MODELS=("chatgpt" "claude" "gemini")                                                                                                                            # List of models to test
CHALLENGES=("todo_list")                                                                                                                                        # List of projects to test
PROMPTS=("1-zero_shot" "2-few_shot" "3-chain_of_thoughts-zero_shot" "4-chain_of_thoughts-few_shot" "5-role-zero_shot" "6-role-few_shot")                        # List of prompts to test
ITERATIONS=10                                                                                                                                                   # Number of iterations of each prompt


# MAIN LOGIC
for challenge in "${CHALLENGES[@]}"
do
    for prompt in "${PROMPTS[@]}"
    do
        for i in $(seq 1 $ITERATIONS)
        do
            echo "$challenge - $prompt - iteration [$i]"

            # Copy test files to the generated folder
            for test in "${ALLTESTS[@]}"
            do
                cp "$TESTS_FOLDER/$challenge/$test.py" "$GENERATED_FOLDER/$challenge/$prompt/iteration_$i/$test.py"
            done

            # Create necessary directories
            mkdir -p "$RESULTS_FOLDER/$challenge/$prompt/iteration_$i"

            # Run all the tests
            for test in "${TESTS[@]}"
            do
                for model in "${MODELS[@]}"
                do
                    python3 "$GENERATED_FOLDER/$challenge/$prompt/iteration_$i/$test.py" "$model" > "$RESULTS_FOLDER/$challenge/$prompt/iteration_$i/$test-$model.txt"
                done
            done

            # Pytest tests
            for pytest in "${PYTESTS[@]}"
            do
                module_name=$(basename $pytest .py | cut -d'-' -f2)
                echo "Testing module: $module_name" > "$RESULTS_FOLDER/$challenge/$prompt/iteration_$i/5_functional_correctness-$module_name.txt"
                python3 -m pytest "$GENERATED_FOLDER/$challenge/$prompt/iteration_$i/$pytest.py" >> "$RESULTS_FOLDER/$challenge/$prompt/iteration_$i/5_functional_correctness-$module_name.txt"
            done

            # Remove test files from the generated folder
            for test in "${ALLTESTS[@]}"
            do
                rm "$GENERATED_FOLDER/$challenge/$prompt/iteration_$i/$test.py"
            done
        done
    done
done