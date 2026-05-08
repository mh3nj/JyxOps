# XML – The Strict Older Sibling of HTML

^_^ Welcome, HTML beast! ^_^

You already know HTML. XML is the same – but stricter, honest, and predictable. No browser forgiving missing closing tags. No unquoted attributes. Just clean, structured data.

:-D Let's begin. :-D


## The Golden Rule (One Sentence)

> **XML is HTML where you invent your own tags, but it's strict – every tag must close, attributes must be quoted, and there's exactly one root element.**


## Chapter 1: Tags – You Already Know This

:-)

```xml
<person>Ali</person>
```

- Opening tag: `<person>`
- Closing tag: `</person>` (the `/` goes before the tag name)
- Content: `Ali`

✅ Correct:
```xml
<name>Hassan</name>
<age>25</age>
```

❌ **Most common mistake #1** – forgetting to close a tag:
```xml
<name>Hassan     <!-- missing </name> → error -->
```

❌ **Common mistake #2** – wrong closing tag order (nesting violation):
```xml
<person><name>Ali</person></name>   <!-- wrong order → error -->
```

**Rule:** Last opened = first closed (just like HTML). :-)


## Chapter 2: Attributes – Like HTML, But Quotes Required

>"<

```xml
<person id="123" status="active">Ali</person>
```

- Attribute names are usually lowercase (not required but convention)
- Values **must** be in double quotes (single quotes also work, but double is standard)

✅ Correct:
```xml
<book id="b1" price="19.99">XML Guide</book>
```

❌ **Common mistake #3** – missing quotes around attribute value:
```xml
<book id=b1>   <!-- error: quotes missing -->
```


## Chapter 3: The Single Root Rule – You Made This Mistake

:-O

**Only one top-level element allowed.**

✅ Correct:
```xml
<library>
  <book>1984</book>
  <book>The Hobbit</book>
</library>
```

❌ **Common mistake** – two roots:
```xml
<students>...</students>
<school>Tehran High School</school>   <!-- second root → error -->
```

**Rule:** Everything must be inside one parent tag. Name it `<data>`, `<root>`, or whatever makes sense. ^_^


## Chapter 4: Self-Closing Tags – Like HTML's `<br/>`

:-P

When an element has no content, you can write it as one tag:

```xml
<break/>
<empty attr="value"/>
```

These are identical to:
```xml
<break></break>
<empty attr="value"></empty>
```

✅ Common use cases:
```xml
<image src="photo.jpg"/>
<line-break/>
<input type="text" value=""/>
```


## Chapter 5: Comments – Exactly Like HTML

<3

```xml
<!-- This is a comment -->
<!-- Comments can span
     multiple lines -->
```

**Rule:** Comments cannot contain `--` inside. And they cannot be nested.


## Chapter 6: Text with Special Characters – Use CDATA

^_^

If your text contains `<`, `>`, `&`, or `]]>`, wrap it in `<![CDATA[ ... ]]>`:

```xml
<code><![CDATA[if (x < 10 && y > 20) { return "hello"; }]]></code>
```

Inside CDATA, **everything is raw text** – no parsing. Useful for code snippets or HTML content.

❌ Without CDATA, this would break:
```xml
<message>5 > 3 & 2 < 4</message>   <!-- error: > and & need escaping -->
```

Better to escape:
```xml
<message>5 &gt; 3 &amp; 2 &lt; 4</message>
```

**Common escape sequences:**
- `&lt;` = `<`
- `&gt;` = `>`
- `&amp;` = `&`
- `&apos;` = `'`
- `&quot;` = `"`

But CDATA is cleaner for large blocks. :-D


## Chapter 7: Naming Rules – Be Careful

:-O

- Tag names can contain letters, digits, hyphens, underscores, periods
- **Cannot** start with "xml" (any case), or a digit, or contain spaces
- Case-sensitive: `<Book>` ≠ `<book>`

✅ Valid: `<book-title>`, `<student_id>`, `<name2>`, `<Hello.World>`

❌ Invalid: `<2ndBook>`, `<xml tag>`, `<book title>`


## Chapter 8: Empty vs Null – No Concept of Null

:"<

In XML, you cannot represent `null` directly. Common workarounds:
- Empty element: `<middle-name></middle-name>` or `<middle-name/>`
- Omit the element entirely
- Use attribute `xsi:nil="true"` (requires XML Schema)

For most configs, just omit missing values. ^_^


## Chapter 9: Processing Instructions & Declaration (Advanced but Common)

:-)

The XML declaration (optional but recommended):
```xml
<?xml version="1.0" encoding="UTF-8"?>
```
- Must be on line 1, column 1 if included
- No spaces before it

Processing instructions (custom instructions for applications):
```xml
<?php echo "hello"; ?>
```


## Chapter 10: Common Mistakes That Will Haunt You

:-P

| Mistake | Wrong | Right |
|---------|-------|-------|
| Missing closing tag | `<name>Ali` | `<name>Ali</name>` |
| Unquoted attribute | `<tag id=123>` | `<tag id="123">` |
| Two roots | `<a></a><b></b>` | `<root><a></a><b></b></root>` |
| Wrong case closing | `<Name>Ali</name>` | `<Name>Ali</Name>` |
| Spaces in tag name | `<book title>` | `<bookTitle>` or `<book-title>` |
| Nested error | `<a><b></a></b>` | `<a><b></b></a>` |


## Practice Exercises (With Answers)

<3

### Exercise 1 (Easy)

Convert this Python to XML:

```python
{
  "person": {
    "first_name": "Leila",
    "last_name": "Hosseini",
    "age": 28
  }
}
```

<details>
<summary>Answer ^_^</summary>

```xml
<person>
  <first_name>Leila</first_name>
  <last_name>Hosseini</last_name>
  <age>28</age>
</person>
```
</details>


### Exercise 2 (Attributes)

Convert to XML. Use `id` as attribute for each product:

```python
{
  "products": [
    {"id": 101, "name": "Laptop", "price": 1200},
    {"id": 102, "name": "Mouse", "price": 25}
  ]
}
```

<details>
<summary>Answer :-D</summary>

```xml
<products>
  <product id="101">
    <name>Laptop</name>
    <price>1200</price>
  </product>
  <product id="102">
    <name>Mouse</name>
    <price>25</price>
  </product>
</products>
```
</details>


### Exercise 3 (CDATA)

Write XML for a `note` element that contains: `"Use <b>bold</b> in HTML & keep < > symbols"`

<details>
<summary>Answer :-O</summary>

```xml
<note><![CDATA[Use <b>bold</b> in HTML & keep < > symbols]]></note>
```

Or escaped:
```xml
<note>Use &lt;b&gt;bold&lt;/b&gt; in HTML &amp; keep &lt; &gt; symbols</note>
```
</details>


### Exercise 4 (Self-Closing)

Write an XML element for an `image` with attributes `src="photo.jpg"` and `width="100"`, no content.

<details>
<summary>Answer :-P</summary>

```xml
<image src="photo.jpg" width="100"/>
```
</details>


### Exercise 5 (Find the Errors – Exam)

This XML is broken. Fix it:

```xml
<?xml version="1.0"?>
<students>
  <student id=101>
    <name>Reza</age>
    <grade>A+</grade>
  </student>
  <student id="102">
    <name>Sara</name>
  </student>
</students>
<school>Test</school>
```

<details>
<summary>Answer ^_^</summary>

```xml
<?xml version="1.0"?>
<root>
  <students>
    <student id="101">
      <name>Reza</name>
      <grade>A+</grade>
    </student>
    <student id="102">
      <name>Sara</name>
    </student>
  </students>
  <school>Test</school>
</root>
```

Errors fixed:
- Missing quotes around `id=101` → `id="101"`
- Mismatched `<name>Reza</age>` → `</name>`
- Second root `<school>` → put inside a single root element
</details>


### Exercise 6 (Your Turn – Mixed)

Convert this Python to XML. Use your own tag names. Include an attribute for each book (e.g., `isbn`).

```python
{
  "library": {
    "name": "Central Library",
    "books": [
      {"title": "Python Crash Course", "isbn": "123", "available": true},
      {"title": "XML for Beginners", "isbn": "456", "available": false}
    ]
  }
}
```

<details>
<summary>Answer :-)</summary>

```xml
<library>
  <name>Central Library</name>
  <books>
    <book isbn="123" available="true">
      <title>Python Crash Course</title>
    </book>
    <book isbn="456" available="false">
      <title>XML for Beginners</title>
    </book>
  </books>
</library>
```
</details>


## Quick Reference Card

^_^

| Need | Write |
|------|-------|
| Element with content | `<tag>text</tag>` |
| Element with child | `<parent><child/></parent>` |
| Attribute | `<tag attr="value">` |
| Self-closing | `<empty/>` |
| Comment | `<!-- comment -->` |
| CDATA (raw text) | `<![CDATA[ raw ]]>` |
| Declaration | `<?xml version="1.0"?>` |


## Final Truth

:-D

XML is **not** trying to trick you. It's just strict. If you remember:

1. **One root**
2. **Close every tag**
3. **Quote attributes**
4. **Case matters**

…you will never fail. And unlike YAML, XML won't randomly break because of indentation or colons. It's honest.

:-) You're now ready for JSON – which is even simpler. No closing tags, no attributes. Just Python-looking dictionaries and lists with double quotes. You'll learn it in 10 minutes. :-)

---

*This tutorial is part of the JyxOps documentation – a tool that converts between YAML, JSON, and XML with zero hassle. Check it out on GitHub!*

^_^ Happy coding! ^_^
