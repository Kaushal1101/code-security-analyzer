import json
import pprint

with open("bandit_report.json", "r") as f:
    data = json.load(f)

delete_list = ["col_offset", "end_col_offset", "line_range"]
rename_dict = {"code": "code_snippet", 
               "issue_confidence": "confidence", 
               "issue_severity": "severity",
               "issue_cwe": "CWE",
               "issue_info": "message"
               }


for result in data["results"]:
    for key in delete_list:
        result.pop(key, None)
    
    for old_key, new_key in rename_dict.items():
        if old_key in result:
            result[new_key] = result.pop(old_key)
    


pprint.pprint(data["results"][0])
