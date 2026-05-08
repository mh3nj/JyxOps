# JSON – The Honest Data Format (No Surprises)

^_^ Welcome, brave learner! ^_^

You've survived YAML's indentation traps and XML's angle bracket chaos. Now meet **JSON** – the data format that never lies, never tricks you, and always does what you expect.

:-D Let's begin. :-D


## The Honest Truth

Remember that scary recursive XML function earlier? Forget it. :-P

For 99% of real work, you use libraries like `json` (built-in), `pyyaml`, or `xmltodict`. You don't need to write parsers. You don't need to understand recursion. You just need to know **the rules**.

And JSON has only **six rules**.

:-) That's it. Six. :-)


## What is JSON?

> "JavaScript Object Notation" – but don't let the name scare you. There's no JavaScript required. :-O

JSON is a **text representation** of:
- dictionaries (`{}`)
- lists (`[]`)
- strings (`""`)
- numbers (`42` or `3.14`)
- booleans (`true` / `false`)
- null (`null`)

Every JSON document is **almost** a valid Python literal. Almost.

:"<


## JSON vs Python – The Only Differences

^_^ Learn this table. It's the whole course. ^_^

| Python | JSON | Example |
|--------|------|---------|
| `True` | `true` | `{"active": true}` |
| `False` | `false` | `{"active": false}` |
| `None` | `null` | `{"value": null}` |
| `'single quotes'` | `"double quotes only"` | `{"name": "Ali"}` |
| `(1, 2, 3)` | `[1, 2, 3]` (no tuples) | lists only |
| trailing commas allowed | **no trailing commas** | `[1, 2, 3]` not `[1, 2, 3,]` |
| comments (`#`) | **no comments** | – |

That's it. **Six differences.** Memorize them and you know JSON.

:-P


## The Entire JSON Tutorial in 5 Lines

<3

```json
{
  "library": {
    "name": "Central Library",
    "books": [
      {"title": "Python 101", "available": true},
      {"title": "XML Mastery", "available": false}
    ]
  }
}
```

That's valid JSON. And it's almost identical to Python. You already know it. ^_^


## Python `json` Module – Only Two Functions You Need

:-D

```python
import json

# Python dict → JSON string
data = {"name": "Ali", "age": 25, "active": True, "score": None}
json_string = json.dumps(data, indent=2)
print(json_string)
# {
#   "name": "Ali",
#   "age": 25,
#   "active": true,
#   "score": null
# }

# JSON string → Python dict
original = json.loads(json_string)
print(original)  # {'name': 'Ali', 'age': 25, 'active': True, 'score': None}
```

### File I/O (Just as Easy)

```python
# Write Python dict to JSON file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Read JSON file to Python dict
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

> "That's everything. No recursion. No custom parsers. Just two functions." :-)


## JSON Data Types (Exactly 6)

^_^

| JSON Type | Python Type | Example |
|-----------|-------------|---------|
| object | dict | `{"name": "Ali"}` |
| array | list | `[1, 2, 3]` |
| string | str | `"hello"` |
| number | int / float | `42` or `3.14` |
| boolean | bool | `true` / `false` |
| null | None | `null` |

No tuples. No sets. No custom objects. **Simple by design.** :")


## Quick Reference Card

:-D Put this on your wall. :-D

| Task | Code |
|------|------|
| Dict → JSON string | `json.dumps(d)` |
| JSON string → Dict | `json.loads(s)` |
| Dict → JSON file | `json.dump(d, f, indent=2)` |
| JSON file → Dict | `json.load(f)` |
| Pretty print | `indent=2` |
| Sort keys | `sort_keys=True` |
| Skip non‑ASCII | `ensure_ascii=False` |
| Custom serializer | `default=lambda o: ...` |


## JSON vs YAML vs XML – When to Use What

:-O

| Format | Best For | Why |
|--------|----------|-----|
| **JSON** | APIs, data exchange, machine‑to‑machine | Strict, fast, no ambiguity |
| **YAML** | Configuration files (Docker, Kubernetes, Ansible) | Human‑friendly, supports comments |
| **XML** | Documents, SOAP, complex schemas | Attributes, validation, mature tooling |

Your **JyxOps** converter handles all three. ^_^


## Practice Exercises (With Answers)

<3

### Exercise 1: Basic Conversion

Convert this Python dict to a JSON string:

```python
person = {
    "name": "Sara",
    "age": 28,
    "skills": ["Python", "YAML", "XML"],
    "employed": True,
    "salary": None
}
```

<details>
<summary>Answer :-)</summary>

```json
{
  "name": "Sara",
  "age": 28,
  "skills": ["Python", "YAML", "XML"],
  "employed": true,
  "salary": null
}
```
</details>

---

### Exercise 2: Reading JSON from a string

Parse this JSON string into a Python dict, then print the second product's price.

```json
'{
  "store": "Bookstore",
  "products": [
    {"name": "Notebook", "price": 5.5},
    {"name": "Pen", "price": 1.2}
  ]
}'
```

<details>
<summary>Answer :-)</summary>

```python
import json
data = json.loads('{"store": "Bookstore", "products": [{"name": "Notebook", "price": 5.5}, {"name": "Pen", "price": 1.2}]}')
print(data["products"][1]["price"])  # 1.2
```
</details>

---

### Exercise 3: Write to file

Save the following Python data to `data.json` with indentation 4.

```python
config = {
    "version": 3,
    "services": ["web", "db", "cache"],
    "settings": {"debug": True, "port": 8080}
}
```

<details>
<summary>Answer :-)</summary>

```python
import json
with open("data.json", "w") as f:
    json.dump(config, f, indent=4)
```
</details>

---

### Exercise 4: Read from file and modify

Load `data.json` from exercise 3, change `debug` to `False`, and save back.

<details>
<summary>Answer :-)</summary>

```python
with open("data.json", "r") as f:
    config = json.load(f)
config["settings"]["debug"] = False
with open("data.json", "w") as f:
    json.dump(config, f, indent=4)
```
</details>

---

### Exercise 5: Handle non‑serializable types

What happens if you try to serialize a tuple? How to fix?

```python
obj = {"coordinates": (10, 20)}
```

<details>
<summary>Answer :-O</summary>

`TypeError: Object of type tuple is not JSON serializable`.

Fix: convert tuple to list before serialization.

```python
obj["coordinates"] = list(obj["coordinates"])
json.dumps(obj)  # works
```
</details>

---

### Exercise 6: Custom encoder for datetime

Serialize a dict containing a `datetime` object.

```python
from datetime import datetime
event = {"name": "meeting", "time": datetime.now()}
```

<details>
<summary>Answer ^_^</summary>

```python
def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

json_str = json.dumps(event, default=json_serial)
# {"name": "meeting", "time": "2025-04-02T12:34:56"}
```
</details>

---

### Exercise 7: Pretty print vs compact

Compare `indent=None` vs `indent=2`.

```python
big = {"a": 1, "b": [2,3,4]}
print(json.dumps(big))           # {"a": 1, "b": [2, 3, 4]}
print(json.dumps(big, indent=2)) # multiline human-readable
```

---

### Exercise 8: Validate JSON string

Write a function that returns `True` if a string is valid JSON, else `False`.

<details>
<summary>Answer :-P</summary>

```python
def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False
```
</details>

---

### Exercise 9: Merge two JSON objects

Merge `a` and `b` (b overrides a for same keys).

```python
a = '{"name": "Ali", "age": 25}'
b = '{"age": 26, "city": "Tehran"}'
```

<details>
<summary>Answer ^_^</summary>

```python
data_a = json.loads(a)
data_b = json.loads(b)
data_a.update(data_b)
merged = json.dumps(data_a)  # {"name": "Ali", "age": 26, "city": "Tehran"}
```
</details>

---

### Exercise 10: Convert JSON to Python and back (round trip)

Ensure that converting Python → JSON → Python returns the original structure.

<details>
<summary>Answer :-D</summary>

```python
original = {"name": "Leila", "scores": [19, 20, 18], "active": True}
json_str = json.dumps(original)
back = json.loads(json_str)
assert original == back  # True
print("Round trip successful!")
```
</details>


## The Mega Converter Approach

:-) No need to write recursive nightmares. Just use libraries. :-)

| From → To | Difficulty | Library |
|-----------|------------|---------|
| Python ↔ JSON | ⭐ | `json` (built‑in) |
| Python ↔ YAML | ⭐⭐ | `pyyaml` |
| Python ↔ XML | ⭐⭐⭐⭐ | `dicttoxml` + `xmltodict` |
| JSON ↔ YAML | ⭐⭐ | Convert through Python |
| XML ↔ anything else | ⭐⭐⭐⭐ | Use Python as intermediate |

```python
import json, yaml, dicttoxml, xmltodict

# Python → JSON
json_str = json.dumps(data)

# Python → YAML
yaml_str = yaml.dump(data)

# Python → XML
xml_bytes = dicttoxml.dicttoxml(data)

# And back again (via Python dict)
data = json.loads(json_str)
data = yaml.safe_load(yaml_str)
data = xmltodict.parse(xml_bytes)
```

That's it. No recursion. No pain. :")


## Final Truth

^_^ <3

- **JSON is strict but honest.** No indentation tricks, no ambiguous colons, no multi‑line magic.
- You already know 95% because it's almost Python.
- Use JSON for **APIs, config files, data exchange** when you don't need comments or single quotes.
- Use YAML when humans need to write configs with comments.
- Use XML when you need attributes or schema validation.

:-D Now go forth and convert everything. :-D

---

*This tutorial is part of the JyxOps documentation – a tool that converts between YAML, JSON, and XML with zero hassle. Check it out on GitHub!*

^_^ Happy coding! ^_^
