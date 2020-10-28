import pprint
import yaml
from jsonpath_ng import jsonpath, parse


def format(response, output):
    if output.startswith('jsonpath'):
        output = output.split('=')[-1].strip('"')
        jsonpath_expr = parse(output)
        for i in [match.value for match in jsonpath_expr.find(response)]:
            print(i)
    elif output.startswith('yaml'):
        print(yaml.dump(response, default_flow_style=False))
    else:
        pprint.pprint(response)