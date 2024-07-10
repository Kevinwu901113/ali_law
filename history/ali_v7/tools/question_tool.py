def tools():
    tools = [
    {
        "type": "function",
        "function": {
            "name": "company_question",
            "description": "根据公司名称获得该公司所有基本信息,包括公司名称、简称、英文名称、关联证券、公司代码、曾用简称、所属市场、所属行业、上市日期、法人代表、总经理、董秘 、邮政编码 、注册地址 、办公地址 、联系电话 、传真 、官方网址 、电子邮箱 、入选指数 、主营业务 、经营范围 、机构简介 、每股面值 、首发价格 、首发募资净额 、首发主承销商",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "公司基本信息某个字段名",
                    },
                    "value": {
                        "type": "string",
                        "description": "公司基本信息某个字段的具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "register_question",
            "description": "根据公司名称获得该公司所有注册信息，包括公司名称、登记状态、统一社会信用代码、注册资本、成立日期、省份、城市、区县、注册号、组织机构代码、参保人数、企业类型、曾用名,",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "公司注册信息某个字段名",
                    },
                    "value": {
                        "type": "string",
                        "description": "公司注册信息某个字段的具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sub_company_question",
            "description": "关联公司的子公司的问题，通常在问题内会包含子公司等字样",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "关联公司或者子公司的某个字段名",
                    },
                    "value": {
                        "type": "string",
                        "description": "关联公司或者子公司的某个字段的具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
        {
            "type": "function",
            "function": {
                "name": "law_question",
                "description": "解决关于法案信息的问题，问题内通常包含法律案号",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "法案信息某个字段名,通常为案号",
                        },
                        "value": {
                            "type": "string",
                            "description": "法案信息某个字段的具体值,当字段为案号时，请保证开头含有左括号",
                        }
                    },
                    "required": ["key","value"],
                },
            }
        },
        {
        "type": "function",
        "function": {
            "name": "open_question",
            "description": "解决开放性问题，例如：我国法律监督体系的构成",
            "parameters": {
                "type": "object",
                "properties": {
                    "problem":{
                        "type": "string",
                        "description": "常识性不需要从知识库查询的问题",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
]
    return tools
