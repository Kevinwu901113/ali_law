def tools():
    tools = [
    {
        "type": "function",
        "function": {
            "name": "search_company_name_by_info",
            "description": "根据公司基本信息某个字段是某个值来查询具体的公司名称",
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
            "name": "get_company_info",
            "description": "根据公司名称获得该公司所有基本信息,包括公司名称、简称、英文名称、关联证券、公司代码、曾用简称、所属市场、所属行业、上市日期、法人代表、总经理、董秘 、邮政编码 、注册地址 、办公地址 、联系电话 、传真 、官方网址 、电子邮箱 、入选指数 、主营业务 、经营范围 、机构简介 、每股面值 、首发价格 、首发募资净额 、首发主承销商",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "公司名称",
                    }
                },
                "required": ["company_name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_register",
            "description": "根据公司名称获得该公司所有注册信息，包括公司名称、登记状态、统一社会信用代码、注册资本、成立日期、省份、城市、区县、注册号、组织机构代码、参保人数、企业类型、曾用名",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "公司名称",
                    }
                },
                "required": ["company_name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_company_name_by_register",
            "description": "根据公司注册信息某个字段是某个值来查询具体的公司名称",
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
            "name": "get_sub_company_info",
            "description": "根据子公司名称获得该公司所有母公司信息，关联上市公司就是母公司，包括关联上市公司股票代码、关联上市公司股票简称、关联上市公司全称、上市公司关系、上市公司参股比例、上市公司投资金额、公司名称",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "子公司名称",
                    }
                },
                "required": ["company_name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_company_name_by_sub_info",
            "description": "根据母公司信息某个字段是某个值来查询所有子公司名称，关联上市公司就是母公司，（包括关联上市公司股票代码、关联上市公司股票简称、关联上市公司全称、上市公司关系、上市公司参股比例、上市公司投资金额、公司名称）",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "母公司信息某个字段名",
                    },
                    "value": {
                        "type": "string",
                        "description": "母公司信息某个字段的具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_legal_document",
            "description": "根据案号(案号格式示例：(2019)冀0203民初5480号)获得该案所有基本信息，包括标题、案号、文书类型、原告、被告、原告律师、被告律师、案由、审理法条依据、涉案金额、判决结果、胜诉方、文件名",
            "parameters": {
                "type": "object",
                "properties": {
                    "case_num": {
                        "type": "string",
                        "description": "案号",
                    }
                },
                "required": ["case_num"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_case_num_by_legal_document",
            "description": "根据法律文书某个字段是某个值来查询具体的案号",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "法律文书某个字段名",
                    },
                    "value": {
                        "type": "string",
                        "description": "法律文书某个字段的具体值",
                    }
                },
                "required": ["key","value"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_connect_company",
            "description": "根据子公司名称元组,格式为(公司a,公司b,公司c)一次性查询子公司和母公司的所有关联信息，包括关联上市公司股票代码、关联上市公司股票简称、关联上市公司全称（外键，关联公司基本信息数据表中的公司名称）、上市公司关系、上市公司参股比例（母公司在子公司的参股比例）、上市公司投资金额、公司名称（外键，关联公司基本信息数据表中的公司名称）",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "tuple",
                        "description": "子公司名称元组",
                    }
                },
                "required": ["company_name"],
            },
        }
    }
]
    return tools