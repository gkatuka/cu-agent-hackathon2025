import json
from fpdf import FPDF

def get_field_result(field,cu_output_path):
    try:
        with open(cu_output_path, "r") as json_file:
            results= json.load(json_file)  # Load JSON data
            return results['result']['contents'][0]['fields'][field]['valueString']  # Extract the field result value
    except FileNotFoundError:
        print(f"Error: File '{cu_output_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{cu_output_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def get_field_description(field,analyzer_path):
    try:
        with open(analyzer_path, "r") as json_file:
            data = json.load(json_file)  # Load JSON data
            return data.get('fieldSchema').get('fields').get(field)['description']  # Extract the field value
    except FileNotFoundError:
        print(f"Error: File '{analyzer_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{analyzer_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def update_field(file_path, field_name, new_value, counter):

    try:
        # Read the existing JSON file
        with open(file_path, "r") as json_file:
            data = json.load(json_file)  # Load JSON data

        # Update the specified field
        if field_name in data:
            data['fieldSchema']['fields'][field_name]['description'] = new_value
            print(f"Field '{field_name}' updated to: {new_value}")
        else:
            print(f"Field '{field_name}' not found in the JSON file. Adding it as a new field.")
            data['fieldSchema']['fields'][field_name]['description'] = new_value

        # Save the updated JSON into a new file
        # analyzer_path = r'C:\Users\katukagloria\source\ai_agent_cu\analyzer_update.json'
        analyzer_path =f"./analyzer_update_{counter}.json"
        with open(analyzer_path, "w") as json_file:
            json.dump(data, json_file, indent=4)  # Save with indentation for readability

        print(f"Updated JSON file saved at: {analyzer_path}")
        return analyzer_path

    except FileNotFoundError:
        print(f"Error: File '{analyzer_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{analyzer_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return

def format_output_json(content):
    try:
        json_str = content.replace('```json\n', '').replace('\n```', '')
        # json_str = content.strip().replace('\n', '').replace('    ', '')
        # Convert the stripped string back to a JSON object to ensure it is valid JSON and to format it neatly
        json_obj = json.loads(json_str)
        formatted_json = json.dumps(json_obj, indent=4)
        
        return formatted_json
    except json.JSONDecodeError as e:
        return f"JSON decoding error: {e}"
    except Exception as e:
        return f"Error processing content: {e}"
    
def format_schema(doc_content_schema):
    json_str = str(doc_content_schema).strip().replace('\n', '').replace('    ', '')
    json_obj = json.loads(json_str)
    formatted_json = json.dumps(json_obj['fields'], indent=4)
    #create a custom analyzer 
    analyzer_name = "custom_analyzer_test"
    analyzer_description = "Sample audio analytics testing custome analyzer"
    locale = ["en-US"]
    # return_details = "true"
    schema_name = "customAnalyzer"
    
    custom_schema_json = {
    "scenario": "callCenter",
    "description": analyzer_description,
    "config": {
        "returnDetails": True,
        "locales": ["en-US"]
        
    },
    "fieldSchema": {
        "fields": json.loads(formatted_json)
    },
    }
    return custom_schema_json

def format_schema2(doc_content_schema):
    # json_str = str(doc_content_schema).strip().replace('\n', '').replace('    ', '')
    json_obj = json.loads(doc_content_schema)
    formatted_json = json.dumps(json_obj['fields'], indent=4)
    #create a custom analyzer 
    analyzer_name = "custom_analyzer_test"
    analyzer_description = "Sample audio analytics testing custome analyzer"
    locale = ["en-US"]
    # return_details = "true"
    schema_name = "customAnalyzer"
    
    custom_schema_json = {
    "scenario": "callCenter",
    "description": analyzer_description,
    "config": {
        "returnDetails": True,
        "locales": ["en-US"]
        
    },
    "fieldSchema": {
        "fields": json.loads(formatted_json)
    },
    }
    return custom_schema_json

def markdown_to_pdf(markdown_text, output_filename):
    """
    Converts a Markdown text into a structured PDF document.
    
    :param markdown_text: The EHR content in Markdown format.
    :param output_filename: The name of the output PDF file.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Process each line of the Markdown content
    for line in markdown_text.split("\n"):
        line = line.strip()
        
        if line.startswith("# "):  # Main Title
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, line[2:], ln=True, align="C")
            pdf.ln(5)
        elif line.startswith("## "):  # Section Title
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, line[3:], ln=True)
            pdf.ln(2)
        elif line.startswith("- **"):  # Bold List Items
            pdf.set_font("Arial", "B", 12)
            line_content = line.replace("- **", "").replace("**", ": ")
            pdf.cell(0, 8, line_content, ln=True)
        elif line.startswith("*"):  # Italicized Content (e.g., Chief Complaint)
            pdf.set_font("Arial", "I", 12)
            pdf.multi_cell(0, 8, line.replace("*", ""))
            pdf.ln(2)
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):  # Numbered List
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 8, line, ln=True)
        elif line:  # Normal Text
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 8, line)
            pdf.ln(2)

    # Save the generated PDF
    pdf.output(output_filename)    
# def format_schema(doc_content_schema):
#     #create a custom analyzer 
#     analyzer_name = "auto_QA_nx_kg_test"
#     analyzer_description = "Sample audio analytics testing auto_QA-nx"
#     locale = ["en-US"]
#     # return_details = "true"
#     schema_name = "audioQnAnalysis"
    
#     custom_schema_json = {
#     "scenario": "callCenter",
#     "description": analyzer_description,
#     "config": {
#         "returnDetails": True,
#         "locales": ["en-US"]
        
#     },
#     "fieldSchema": {
#         "fields": json.loads(doc_content_schema) 
#     },
#     }
#     # result = "Create_a_formatted_analyzer"
#     # custom_schema_json = json.loads(custom_schema_json)
    
#     # Convert the string into a Python dictionary
#     # parsed_dict = json.loads(input_string)

#     # For the "fields" key inside "fieldSchema", convert its value to a dictionary
#     # custom_schema_json["fieldSchema"]["fields"] = json.loads(custom_schema_json["fieldSchema"]["fields"])
#     # custom_schema_json = json.dumps(custom_schema_json, indent=4)
#     return custom_schema_json

