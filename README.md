# JSON-Generator
Use your terminal to generate JSON files based on templates


## Usage
```bash
python3 jsongen.py (options) <template-file> <repeat> <output-file>
```

## Templates
A template is a .json file, that contains an object.
Let's say you want to generate a database of users. One user looks like this:
```json
{
  "username": "myUsername",
  "password": "myUnhashedPassword"
}
```
To generate random usernames and passwords, you can use built-in functions:
```json
{
  "username": "~username~",
  "password": "~password~"
}
```
Notice, that a function is surrounded by "~".
This character is called the **function operator**.
If we run `jsongen.py`:
```bash
python3 jsongen.py user-template.json 3 all-users.json
```
We generate **3** random user-objects:
```js
[
    {
        "password": "GxzfErXymenp",
        "username": "marge99"
    },
    {
        "password": "QgqmTSsgrquQdt",
        "username": "gene"
    },
    {
        "password": "zNnjkUEYILmtI",
        "username": "rick5"
    }
]
```

## Functions
| name       | description                                | example                                  |
|------------|--------------------------------------------|------------------------------------------|
| username   | Random username                            | rick1337                                 |
| password   | Random 8-16 long password from a-z/A-Z     | koJAjvLYEgzqoIpY                         |
| hash       | Random characters from 0-F                 | fd1bbd7591ae4b2f46bd63f71b6216918cef1722 |
| timestamp  | Random integer timestamp from 1970/1/1-now | 235990744                                |
| ftimestamp | Random float timestamp from 1970/1/1-now   | 685570739.9418381                        |
| now        | Current integer timestamp                  | 1612304012                               |
| fnow       | Current float timestamp                    | 1612304012.9423177                       |
| int        | Random integer from 0-65535                | 51814                                    |
| float      | Random float from 0-65535                  | 46989.959716188394                       |
