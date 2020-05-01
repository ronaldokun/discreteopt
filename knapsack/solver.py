#!/usr/bin/python
# -*- coding: utf-8 -*-
from pathlib import Path
from collections import namedtuple
from typing import *
Item = namedtuple("Item", ['index', 'value', 'weight'])

def parse_input(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    return items, capacity


def iterate(items, max_cost):
    value = 0
    weight = 0
    taken = [0]*len(items)
    
    if max_cost <= 0:
        return value, taken
    
    for item in items:
        if weight + item.weight <= max_cost:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value, taken


def greedy(items: List[Item], max_cost: int, key: Callable)->Tuple[int, List[int]]:
    """Receives a list of items of namedtuples with attributes index, value and weight.
       Sort the items in reverse order by key and get the items until max_cost is reached
    """        
    items_copy = sorted(items, key=key, reverse=True)
    
    return iterate(items_copy, max_cost)


def get_greedy(items, capacity, keyfunc):
    value, taken = greedy(items, capacity, key=keyfunc)
    print(f"Total value of items taken: {value}")
    return value, taken


def test_greedy(input_data):
    
    items = parse_input(input_data)        
    max_  = []
        
    print(f"Use greedy to allocate a weight of {capacity}")
    print('By Value')
    value, taken = get_greedy(items, capacity, lambda x: x.value)
    max_.append((value, taken, 'value'))
    print("="*80)
    print("By Weight")
    value, taken = get_greedy(items, capacity, lambda x: 1 / x.weight)
    max_.append((value, taken, 'weight'))
    print("="*80)
    print("By density")
    value, taken = get_greedy(items, capacity, lambda x: x.value/x.weight)
    max_.append((value, taken, 'density'))
    
    max_.sort(key=lambda x: x[0], reverse=True)
    
    return max_[0]


def depth_first(items, capacity, memo={}):
    item = memo.get((len(items), capacity), None)
    if item:
        result = item        
    elif not len(items) or capacity <= 0:
        result = (0, [])
    elif items[0].weight > capacity:
        #Explore right Branch
        result = depth_first(items[1:], capacity, memo)
    else:
    
        next_item = items[0]

        #Explore left branch
        with_item, taken = depth_first(items[1:], capacity - next_item.weight, memo)    
        with_item += next_item.value

        #Explore right branch
        without_item, not_taken = depth_first(items[1:], capacity, memo)

        if with_item > without_item:
            
            result = (with_item, taken + [next_item])
        else:
            result = (without_item, taken)

        memo[(len(items), capacity)] = result

    return result


# +
# data = Path.cwd() / 'data'
# data = sorted(list(data.iterdir()), key = lambda x: int(str(x).split("_")[-2]))
# for d in data:
#     print(f"Testing file {d.name}")
#     print("->" * 20)
#     input_data = d.read_text()
#     v,t,n = test_greedies(input_data)
#     print(f"The winner is {n}")
#     print("<-" * 20)
# -

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    #value, taken, name = test_greedies(input_data)
    
    items, capacity = parse_input(input_data)
    
    value, items = depth_first(items, capacity)
    
    taken = [0] * len(items)
    
    print(len(taken))
    
    for item in items:
        taken[item.index] = 1
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
        
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')



