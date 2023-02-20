TYPE = {
    "VARCHAR": "string",
    "VARBINARY": "binary",
    "TINYINT": "byte",
    "TIMESTAMP": "timestamp",
    "TIME": "date",
    "SMALLINT": "short",
    "REAL": "double",
    "NUMERIC": "double",
    "LONGVARCHAR": "string",
    "JAVA_OBJECT": "object",
    "INTEGER": "int",
    "FLOAT": "float",
    "DOUBLE": "double",
    "DECIMAL": "big_decimal",
    "DATE": "date",
    "CLOB": "string",
    "CHAR": "string",
    "BOOLEAN": "boolean",
    "BLOB": "binary",
    "BIT": "byte",
    "BINARY": "binary",
    "BIGINT": "big_integer",
    "CHARACTER": "string",
    "CHARACTER VARYING": "string",
    "TEXT": "string",
}

SPECIAL_NODES = [
    "encrypt",
    "hash",
    "mask"
]

SPECIAL_NODES_PATTERN = {
    "encrypt": ["Email", "Location data", "Home address", "IP address"],
    "hash": ["password"],
    "mask": ["number"],
}
