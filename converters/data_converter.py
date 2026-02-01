"""Data converter module"""
import json
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from pathlib import Path

def convert(input_file, output_file, target_format):
    """
    Convert data files between formats
    Supports: JSON ↔ CSV ↔ XML
    """
    try:
        input_ext = Path(input_file).suffix.lower().lstrip('.')
        target_format = target_format.lower()
        
        # Read input data
        data = None
        
        if input_ext == 'json':
            data = read_json(input_file)
        elif input_ext == 'csv':
            data = read_csv(input_file)
        elif input_ext == 'xml':
            data = read_xml(input_file)
        else:
            print(f"Unsupported input format: {input_ext}")
            return False
        
        if data is None:
            return False
        
        # Write output data
        if target_format == 'json':
            return write_json(data, output_file)
        elif target_format == 'csv':
            return write_csv(data, output_file)
        elif target_format == 'xml':
            return write_xml(data, output_file)
        else:
            print(f"Unsupported output format: {target_format}")
            return False
    
    except Exception as e:
        print(f"Data conversion error: {e}")
        return False

def read_json(filepath):
    """Read JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON read error: {e}")
        return None

def read_csv(filepath):
    """Read CSV file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"CSV read error: {e}")
        return None

def read_xml(filepath):
    """Read XML file"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Convert XML to list of dictionaries
        data = []
        for item in root:
            row = {}
            for child in item:
                row[child.tag] = child.text
            data.append(row)
        
        return data
    except Exception as e:
        print(f"XML read error: {e}")
        return None

def write_json(data, filepath):
    """Write JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"JSON write error: {e}")
        return False

def write_csv(data, filepath):
    """Write CSV file"""
    try:
        if not data:
            return False
        
        # Handle list of dicts
        if isinstance(data, list) and data and isinstance(data[0], dict):
            keys = data[0].keys()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            return True
        
        # Handle simple list or dict
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if isinstance(data, dict):
                writer.writerow(['key', 'value'])
                for key, value in data.items():
                    writer.writerow([key, value])
            else:
                for item in data:
                    writer.writerow([item])
            return True
    
    except Exception as e:
        print(f"CSV write error: {e}")
        return False

def write_xml(data, filepath):
    """Write XML file"""
    try:
        root = ET.Element('data')
        
        if isinstance(data, list):
            for item in data:
                item_elem = ET.SubElement(root, 'item')
                if isinstance(item, dict):
                    for key, value in item.items():
                        child = ET.SubElement(item_elem, str(key))
                        child.text = str(value)
                else:
                    item_elem.text = str(item)
        elif isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(root, str(key))
                child.text = str(value)
        
        # Pretty print XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        return True
    
    except Exception as e:
        print(f"XML write error: {e}")
        return False
