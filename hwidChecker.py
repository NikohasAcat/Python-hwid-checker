import os
import json
import wmi
import sys

def get_processor_id():
    try:
        wmi_obj = wmi.WMI()
        for processor in wmi_obj.Win32_Processor():
            return processor.ProcessorId.strip()
    except Exception as e:
        print("Error:", e)
        return None

def save_hwid_to_json(processor_id):
    data = {"processor_id": processor_id}
    with open("hwid.json", "w") as file:
        json.dump(data, file, indent=4)

def load_hwid_from_json():
    if os.path.exists("hwid.json"):
        with open("hwid.json", "r") as file:
            return json.load(file)
    else:
        return None

def check_hwid_match(processor_id):
    saved_hwid = load_hwid_from_json()
    if saved_hwid:
        if saved_hwid["processor_id"] != processor_id:
            print("HWID mismatch. Exiting program.")
            sys.exit(1)
    else:
        save_hwid_to_json(processor_id)

processor_id = get_processor_id()
if processor_id:
    print("Processor ID:", processor_id)
    check_hwid_match(processor_id)
    print("HWID verified.")
else:
    print("Failed to retrieve Processor ID.")
