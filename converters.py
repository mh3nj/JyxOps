# converters.py
import json
import yaml
import xmltodict
from xml.dom import minidom

def yaml_to_dict(s):
    return yaml.safe_load(s)

def dict_to_yaml(d, indent=2):
    return yaml.dump(d, default_flow_style=False, indent=indent, allow_unicode=True)

def json_to_dict(s):
    return json.loads(s)

def dict_to_json(d, indent=2):
    return json.dumps(d, indent=indent, ensure_ascii=False)

def xml_to_dict(s):
    return xmltodict.parse(s)

def dict_to_xml(data, root_tag="root"):
    """Convert Python dict to XML. Lists become repeated elements with id attributes."""
    def add_ids(obj, path=""):
        if isinstance(obj, list):
            for idx, item in enumerate(obj, start=1):
                if isinstance(item, dict):
                    item["@id"] = str(idx)
                else:
                    obj[idx-1] = {"@id": str(idx), "#text": item}
            for item in obj:
                add_ids(item, path)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                add_ids(v, path + "/" + k)
        return obj

    if not isinstance(data, dict):
        data = {root_tag: data}
    else:
        data = {root_tag: data}
    import copy
    processed = copy.deepcopy(data)
    add_ids(processed)
    return xmltodict.unparse(processed, pretty=True)