# YAML – The Friendly Data Format That Lies to You (But We'll Fix That)

^_^ Welcome, brave soul! ^_^

You've mastered JSON (honest) and XML (strict). Now meet YAML – the format that looks like Python, acts like Python, but has a few... surprises.

:-D Don't worry. After this tutorial, you'll never be confused by YAML again. :-D


## The Golden Rule

> **YAML is Python without commas, brackets, or quotes – but with strict indentation and dashes for lists.**

:-) Remember this. It will save you. :-)


## Chapter 1: Basic Key-Value (Dictionary)

^_^

✅ Correct:
```yaml
name: Ali
age: 25
```
→ Python: `{"name": "Ali", "age": 25}`

❌ **Most common mistake #1** – missing space after colon:
```yaml
name:Ali        # Wrong! Need space after colon
name:  Ali      # Two spaces? Also fine, but one is enough
```

**Rule:** `key: value` – one space after colon. Always. :-P


## Chapter 2: Lists – Use Dashes (`-`)

:-)

✅ Correct:
```yaml
fruits:
  - apple
  - banana
  - cherry
```
→ Python: `{"fruits": ["apple", "banana", "cherry"]}`

❌ **Most common mistake #2** (everyone makes this):
```yaml
fruits:
  apple        # No dash → YAML thinks 'apple' is a key, not a list item
  banana
```

**Rule:** Every list item MUST start with `- ` (dash + space) on a new line. :-O


## Chapter 3: Nested Dictionaries – Indent with Spaces (Never Tabs)

:">

✅ Correct:
```yaml
person:
  name: Sara
  address:
    street: Valiasr
    city: Tehran
```
→ Python: `{"person": {"name": "Sara", "address": {"street": "Valiasr", "city": "Tehran"}}}`

❌ **Common mistake #3** – mixing tabs or inconsistent spaces:
```yaml
person:
	name: Sara      # Tab instead of spaces → some parsers crash
    address:       # 4 spaces
      street: Valiasr   # 2 spaces → inconsistent
```

**Rule:** Use **2 spaces** for each level. Be consistent everywhere. Your life depends on it. :-P


## Chapter 4: Lists of Dictionaries (Very Common in Real Configs)

:-D

✅ Correct:
```yaml
students:
  - name: Ali
    age: 20
  - name: Sara
    age: 22
```
→ Python: `{"students": [{"name": "Ali", "age": 20}, {"name": "Sara", "age": 22}]}`

❌ **Common mistake #4** – missing dash for second item:
```yaml
students:
  - name: Ali
    age: 20
  name: Sara      # Missing dash → now 'name' is a key inside 'students'
    age: 22
```

**Rule:** Each new dictionary in a list gets its own `- ` on a new line. ^_^


## Chapter 5: Multi-Line Strings – Use `|` or `>`

:-)

- `|` (pipe) = keep all line breaks (literal block)
- `>` (greater than) = fold lines into one space (except blank lines)

✅ Correct:
```yaml
description: |
  Line one
  Line two
```
→ Python: `{"description": "Line one\nLine two\n"}`

```yaml
description: >
  This entire
  thing becomes
  one line.
```
→ Python: `{"description": "This entire thing becomes one line.\n"}`

❌ **Common mistake #5** – no indentation after `|` or `>`:
```yaml
description: |
Line one        # No indentation → YAML thinks 'Line' is a new key
Line two
```

**Rule:** After `|` or `>`, all lines of text **must be indented** (relative to the key). :"<


## Chapter 6: Strings with Colons (`:`) or Special Characters – Use Quotes

^_^

✅ Correct:
```yaml
command: "docker run -p 8080:80 nginx"
message: "Status: OK\nTime: 12:00"
url: "https://example.com:8080"
```

❌ **Common mistake #6** – colon without quotes:
```yaml
message: Status: OK   # YAML sees second colon → parsing error
```

**Rule:** If a string contains `: ` (colon + space), `#`, `@`, `\n`, or `{}[]`, put **double quotes** around it. :-O


## Chapter 7: Booleans and Null – Use Lowercase

:-D

✅ Correct:
```yaml
enabled: true
disabled: false
empty: null
also_empty: ~
```
→ Python: `{"enabled": True, "disabled": False, "empty": None, "also_empty": None}`

❌ **Common mistake #7**:
```yaml
enabled: True     # Some parsers accept, but not all. Use lowercase 'true'
empty: None       # Python None is not YAML – use 'null' or '~'
```

**Rule:** `true`, `false`, `null`, `~` – lowercase only. ^_^


## Chapter 8: Inline Lists and Dictionaries (Shortcut)

:-)

✅ Valid (but less readable):
```yaml
ports: [80, 443]
env: {NODE_ENV: production, PORT: 8080}
```

**Rule:** Use multi-line for clarity unless the list/dict is very short (1-3 items). :-P


## Chapter 9: Anchors (`&`) and Aliases (`*`) – Reuse Data

:-O

✅ Correct:
```yaml
defaults: &defaults
  timeout: 30
  retry: 3
production:
  <<: *defaults
  url: prod.example.com
```
→ `production` inherits `timeout: 30` and `retry: 3` from `defaults`

**Rule:** `&name` marks a block, `*name` reuses it, `<<:` merges mappings. :-)


## Chapter 10: Start/End Markers – You Can Ignore Them

:-P

- `---` separates multiple YAML documents in one file
- `...` ends a document
- **You don't need them** for 99% of config files


## The YAML ↔ Python Cheat Sheet

^_^ Put this on your wall. ^_^

| What you want | YAML | Python equivalent |
|---------------|------|--------------------|
| Simple key-value | `name: Ali` | `{"name": "Ali"}` |
| List | `- item` | `["item"]` |
| Nested dict | `parent:`<br>`  child: value` | `{"parent": {"child": "value"}}` |
| List of dicts | `- key: val` | `[{"key": "val"}]` |
| Multi-line (keep breaks) | `text: \|`<br>`  Line1`<br>`  Line2` | `"Line1\nLine2\n"` |
| Multi-line (fold) | `text: >`<br>`  Line1`<br>`  Line2` | `"Line1 Line2\n"` |
| String with colon | `"time: 12:00"` | `"time: 12:00"` |
| Boolean true | `true` | `True` |
| Boolean false | `false` | `False` |
| Null | `null` or `~` | `None` |


## Practice Exercises (With Answers)

<3

### Exercise 1: Basic Conversion

Convert this Python dict to YAML:

```python
{
  "name": "Sara",
  "age": 28,
  "skills": ["Python", "YAML", "XML"],
  "employed": true,
  "salary": null
}
```

<details>
<summary>Answer ^_^</summary>

```yaml
name: Sara
age: 28
skills:
  - Python
  - YAML
  - XML
employed: true
salary: null
```
</details>


### Exercise 2: Nested Dictionaries

Convert this Python to YAML:

```python
{
  "person": {
    "name": "Reza",
    "address": {
      "city": "Tehran",
      "zip": 12345
    }
  }
}
```

<details>
<summary>Answer :-D</summary>

```yaml
person:
  name: Reza
  address:
    city: Tehran
    zip: 12345
```
</details>


### Exercise 3: List of Dictionaries

Convert this Python to YAML:

```python
{
  "users": [
    {"name": "Alice", "age": 30, "active": true},
    {"name": "Bob", "age": 25, "active": false}
  ]
}
```

<details>
<summary>Answer ^_^</summary>

```yaml
users:
  - name: Alice
    age: 30
    active: true
  - name: Bob
    age: 25
    active: false
```
</details>


### Exercise 4: Multi-line String

Convert this Python to YAML (use `|`):

```python
{
  "message": "Line one\nLine two\nLine three"
}
```

<details>
<summary>Answer :-)</summary>

```yaml
message: |
  Line one
  Line two
  Line three
```
</details>


### Exercise 5: Find the Errors

This YAML is broken. Fix it:

```yaml
users:
 - name: Alice
    age: 30
    active: True
 - name: Bob
   age: 25
   active: false

config:
  timeout: 60
  - paths:
    /tmp
    /var/log
```

<details>
<summary>Answer :-O</summary>

```yaml
users:
  - name: Alice
    age: 30
    active: true
  - name: Bob
    age: 25
    active: false

config:
  timeout: 60
  paths:
    - /tmp
    - /var/log
```

Errors fixed:
- Indentation under `users` – `age` and `active` must align with `name`
- `True` → `true` (lowercase)
- `- paths:` → `paths:` then list items with `-`
</details>


### Exercise 6: Docker Compose Style

Convert this Python to YAML:

```python
{
  "version": "3",
  "services": {
    "web": {
      "image": "nginx:latest",
      "ports": [80, 443],
      "environment": {
        "NODE_ENV": "production",
        "PORT": "8080"
      }
    }
  }
}
```

<details>
<summary>Answer :-D</summary>

```yaml
version: "3"
services:
  web:
    image: "nginx:latest"
    ports:
      - 80
      - 443
    environment:
      NODE_ENV: production
      PORT: "8080"
```
</details>


## The One Final Truth

^_^

YAML is **indentation-sensitive** just like Python.  
If your YAML doesn't work, 90% of the time it's:

1. **Missing dash** in a list (`- `)
2. **Inconsistent spaces** (use 2 spaces everywhere)
3. **Missing quotes** around a string that contains `: ` or `#`
4. **No space after colon** (`key: value` not `key:value`)

Fix those, and you're a YAML expert. :-D

---

*This tutorial is part of the JyxOps documentation – a tool that converts between YAML, JSON, and XML with zero hassle.*

^_^ Happy coding! ^_^ <3
