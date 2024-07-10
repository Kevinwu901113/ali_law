def tools():
    tools = [
    {
        "type": "function",
        "function": {
            "name": "英文名称",
            "description": "英文名称，通常带有英文字符",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "固定值为英文名称",
                    },
                    "value": {
                        "type": "string",
                        "description": "英文名称具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "公司简称",
            "description": "中文简称，通常为四个字，如鹏鹞环保",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "固定值为公司简称",
                    },
                    "value": {
                        "type": "string",
                        "description": "公司简称具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "公司名称",
            "description": "公司全称，通常带有有限公司等字样",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "固定值为公司名称",
                    },
                    "value": {
                        "type": "string",
                        "description": "公司名称具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
]
    return tools
