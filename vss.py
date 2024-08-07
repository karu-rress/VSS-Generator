import json
import jsonpatch
import random
from typing import Generator, Any

class vss_json:
    """VSS JSON manager class"""
        
    def __init__(self, **kwargs):
        """
        Initialize VSS JSON data
        
        :param kwargs: EITHER of the following is required
            - file: JSON file to load
            - data: JSON data (for internal use)
        """
        assert 'file' in kwargs or 'data' in kwargs
        self.initialized: bool = False        
        
        if 'file' in kwargs:
            with open(kwargs['file'], 'r') as f:
                self.data = json.load(f)  
            self.remove_key('description', 'uuid', 'type', 'comment', 'deprecated')
        elif 'data' in kwargs:
            self.data = kwargs['data']
            self.initialized = True
        else:
            raise ValueError('Either file or data must be provided')
        
    def print(self, indent: int=4, with_index: bool=False) -> None:
        """Print JSON data"""
        txt = json.dumps(self.data, indent=indent)
        if with_index:
            for i, line in enumerate(txt.split('\n'), 1):
                print(f'{i:05d}: {line}')
        else:
            print(txt)
        
    def remove_key(self, *keys: str) -> None:
        """
        Remove keys from JSON data recursively
        
        :param keys: Keys to remove
        """
        for leaf, _ in self.leaf_nodes():
            for key in keys:
                if key in leaf:
                    del leaf[key]
            
    def leaf_nodes(self, data=None, parent_key: str='') -> Generator[tuple[Any, str], None, None]:
        """
        Traverse and yield all leaf values (dict/scaler) in JSON data
        
        :param data: JSON data to traverse (default: self.data)
        :param parent_key: Parent key to track the hierarchy (for debugging and display purposes)
        """
        if data is None:
            data = self.data
        
        if not self.initialized:
            if isinstance(data, dict):
                is_leaf = all(not isinstance(value, dict) for value in data.values())
                if is_leaf:
                    yield data, parent_key
                else:
                    for key, value in data.items():
                        yield from self.leaf_nodes(value, parent_key + '.' + key if parent_key else key)
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    yield from self.leaf_nodes(item, parent_key + f'[{index}]')
        else:
            if isinstance(data, dict):
                for key, value in data.items():
                    yield from self.leaf_nodes(value, parent_key + '.' + key if parent_key else key)
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    yield data, parent_key
            else:
                yield data, parent_key
                
    
    def generate(self, dataset_size: float=1.0) -> tuple['vss_json', 'vss_json']:
        """
        Generate an initial random dataset based on the JSON schema
        
        :param dataset_size: Dataset size ratio [0.0, 1.0]
        """
        result = {}
        
        for leaf, parent in self.leaf_nodes():
            # !! only add the node by dataset_size
            if random.random() > dataset_size:
                continue
            
            # step 1: set parent (without 'children' dictionary)
            hierarchy = [x for x in parent.split('.') if x != 'children']
            new = result
            for idx, node in enumerate(hierarchy):
                if node not in new:
                    new[node] = {}
                    if idx == len(hierarchy) - 1:
                        break
                    new = new[node]
                
            # step 2: set leaf by 'datatype'
            dtype = leaf['datatype']
            if dtype == 'boolean':
                new[node] = random.choice([True, False])
            elif dtype in ['int8', 'uint8', 'float'] and \
                'unit' in leaf and leaf['unit'] == 'percent':
                new[node] = random.random() * 100
                if dtype != 'float':
                    new[node] = int(new[node])
            elif 'allowed' in leaf:
                new[node] = random.choice(leaf['allowed'])
            elif dtype == 'double' or dtype == 'float':
                new[node] = random.random() * 100
            elif dtype == 'float[]':
                new[node] = []
                for i in range(random.randint(1, 5)):
                    new[node].append(random.random() * 100)
            elif dtype in ['int8', 'int16', 'int32']:
                new[node] = random.randint(-100, 100)
            elif dtype == 'string':
                # generate random str`ing
                new[node] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
            elif dtype == 'string[]':
                new[node] = []
                for i in range(random.randint(1, 5)):
                    new[node].append(''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)))
            elif dtype in ['uint8', 'uint16', 'uint32']:
                new[node] = random.randint(0, 100)
            elif dtype == 'uint8[]':
                new[node] = []
                for _ in range(random.randint(1, 5)):
                    new[node].append(random.randint(0, 100))
                    
        return vss_json(data=result), vss_json(data=jsonpatch.make_patch({}, result).patch)
    
    def generate_next(self, change_rate) -> tuple['vss_json', 'vss_json']:
        assert self.initialized, 'vss_json must be initialized with generate()'
        
        result = {}
        for leaf_data, parent in self.leaf_nodes():
            hierarchy = [x for x in parent.split('.') if x != 'children']
            current = result
            for idx, node in enumerate(hierarchy):
                if node not in current:
                    current[node] = {}
                    if idx == len(hierarchy) - 1:
                        break
                    current = current[node]
                    
            if isinstance(leaf_data, list):
                current[node] = leaf_data[:]
                continue        
            
            if random.random() > change_rate:
                current[node] = leaf_data
                continue
            
            match leaf_data:
                case str():
                    current[node] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
                case bool():
                    current[node] = not leaf_data
                case int():
                    current[node] = random.randint(0, 100)
                case float():
                    current[node] = random.random() * 100
        return vss_json(data=result), vss_json(data=jsonpatch.make_patch(self.data, result).patch)
    
    def save(self, file: str) -> None:
        """Save JSON data to file"""
        with open(file, 'w') as f:
            json.dump(self.data, f, indent=4)