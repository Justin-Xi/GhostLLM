import json


def merge(json_file, json_file1, output_file):
    """Compare and merge JSON data from two JSON files."""
    with open(json_file, 'r', encoding='utf-8') as file:
        table_data = json.load(file)

    with open(json_file1, 'r', encoding='utf-8') as file:
        test_spec = json.load(file)

    # Extract actions from test_spec for easier checking
    existing_actions = {task["action"]: task for task in test_spec["tasks"]}

    # Iterate over modules and their functions
    for module, functions in table_data.items():
        for func_name, func_details in functions.items():
            if "name" in func_details:  # Ensure 'name' key exists
                action_name = func_details["name"]
                if "description" in func_details:
                    description = translate_description(func_details["description"])
                else:
                    description = translate_description(func_name)
                    print("No description available.")
                    continue

                if action_name in existing_actions:
                    # Update existing action description
                    existing_actions[action_name]["description"] = description
                else:
                    # Add new action if not found
                    new_task = {
                        "action": action_name,
                        "description": description,
                        "composition": "",
                        "guideline": ""
                    }
                    test_spec["tasks"].append(new_task)

    # Save or print the updated JSON
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(test_spec, file, ensure_ascii=False, indent=2)


def translate_description(description):

    # Placeholder for translation logic
    return description  # Replace with actual translation code/API call


# Example usage
merge("./decription_English.json", "./test_spec.json", "updated_test_spec1.json")
