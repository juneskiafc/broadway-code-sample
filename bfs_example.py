from typing import Dict
from pathlib import Path
import datetime
import re

def convert_config_paths_to_full_paths(root_path: str,
                                       config: dict,
                                       path_key: str ="paths") -> dict:
    """
    Converts all leaf paths under the path_key in config to a full path prepended by root_path.

    E.g.
    if a config.yaml file that is the source of config looks like this:
    
    root_path: /full/path/
    name: something
    paths:
      a: path_1
      b:
        ba: path_2
        bb:
          bba: path_3
    
    Then after processing, the equivalent yaml file for the new config will look like this:

    root_path: /full/path/
    name: something
    paths:
      a: /full/path/path_1
      b:
        ba: /full/path/path_2
        bb:
          bba: /full/path/path_3
    
    If the path_key doesn't exist in the yaml file, then this does nothing.
    """
    if path_key in config:
        paths_dict = prepend_data_path_to_path_dict(data_path=root_path, path_dict=config[path_key])
        config = {**config, **paths_dict}
        del config[path_key]
        
    return config

def prepend_data_path_to_path_dict(data_path: str, path_dict: Dict) -> Dict:
    """
    BFS searches for paths (nodes in the path_dict tree), then converts them to a full path (path -> data_path/path).
    """
    q = [path_dict]

    while len(q) > 0:
        node = q.pop(0)
        for k, v in node.items():
            if isinstance(v, dict):
                q.append(v)
            elif isinstance(v, list):
                node[k] = [Path(data_path).joinpath(elem) for elem in v]
            else:
                if v is not None:
                    node[k] = Path(data_path).joinpath(v)
    
    return path_dict