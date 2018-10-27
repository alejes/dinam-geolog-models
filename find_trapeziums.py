import numpy as np
import pandas as pd
import random

class cache:
    def __init__(self, a, b, ans):
        self.a = a
        self.b = b
        self.ans = ans

def fill_levi(
    a_index, b_index,
    window_sizes,
    compare_penalty_fn,
    delete_penalty_per_point,
    cache
):
    if a_index < 0:
        return b_index * delete_penalty_per_point, a_index, -1
    if b_index < 0:
        return a_index * delete_penalty_per_point, -1, b_index
    
    min_ans = None
    min_ans_a = None
    min_ans_b = None

    #del a letter
    new_a_index = a_index - 1
    if new_a_index >= -1:
        current_ans = cache.ans[new_a_index, b_index] + delete_penalty_per_point
        if min_ans is None or min_ans > current_ans:
            min_ans = current_ans
            min_ans_a = new_a_index
            min_ans_b = b_index
    
    #del b letter
    new_b_index = b_index - 1
    if new_b_index >= -1:
        current_ans = cache.ans[a_index, new_b_index] + delete_penalty_per_point
        if min_ans is None or min_ans > new_b_index:
            min_ans = current_ans
            min_ans_a = a_index
            min_ans_b = new_b_index
    
    #compare a and b letters
    for ws_a in window_sizes:
        new_a_index = a_index - ws_a
        if new_a_index < -1:
            continue
        for ws_b in window_sizes:
            new_b_index = b_index - ws_b
            if new_b_index < -1:
                continue
            
            current_ans = cache.ans[a_index, new_b_index] + compare_penalty_fn(
                new_a_index, new_b_index, ws_a, ws_b
            )

            if min_ans is None or min_ans > current_ans:
                min_ans = current_ans
                min_ans_a = new_a_index
                min_ans_b = new_b_index


    cache.a[a_index, b_index] = min_ans_a
    cache.b[a_index, b_index] = min_ans_b
    cache.ans[a_index, b_index] = min_ans

def find_trapeziums(
    a_types,
    b_types,
    a_pors,
    b_pors
):
    window_sizes = [1, 2, 3, 4, 6, 10]
    delete_penalty_per_point = 0.3
    resize_penalty_per_point = 0.02
    h_penalty = 0.002
    por_penalty = 7
    type_penalty = 2

    avg_por_a_cache = [[None] * len(window_sizes) for i in a_types] 
    avg_por_b_cache = [[None] * len(window_sizes) for i in b_types] 
    avg_type_a_cache = [[None] * len(window_sizes) for i in a_pors] 
    avg_type_b_cache = [[None] * len(window_sizes) for i in b_pors] 
    window_sizes_map = dict()
    for i in range(len(window_sizes)):
        window_sizes_map[window_sizes[i]] = i

    def compare_penalty_fn(i_a, i_b, size_a, size_b):
        i_a += 1
        i_b += 1
        diff_size_penalty = abs(size_a - size_b) * resize_penalty_per_point
        
        diff_h_penalty = abs(i_a - i_b) * h_penalty
        
        size_a_index = window_sizes_map[size_a]
        size_b_index = window_sizes_map[size_b]

        if avg_por_a_cache[i_a][size_a_index] == None:
            avg_por_a_cache[i_a][size_a_index] = sum(a_pors[i_a - size_a : i_a]) * 1.0 / size_a
        if avg_por_b_cache[i_b][size_b_index] == None:
            avg_por_b_cache[i_b][size_b_index] = sum(b_pors[i_b - size_b : i_b]) * 1.0 / size_b
        avg_por_a = avg_por_a_cache[i_a][size_a_index]
        avg_por_b = avg_por_b_cache[i_b][size_b_index]
        diff_por_penalty = por_penalty * abs(avg_por_a - avg_por_b)
        
        if avg_type_a_cache[i_a][size_a_index] == None:
            avg_type_a_cache[i_a][size_a_index] = sum(a_types[i_a - size_a : i_a]) * 1.0 / size_a
        if avg_type_b_cache[i_b][size_b_index] == None:
            avg_type_b_cache[i_b][size_b_index] = sum(b_types[i_b - size_b : i_b]) * 1.0 / size_b
        avg_type_a = avg_type_a_cache[i_a][size_a_index]
        avg_type_b = avg_type_b_cache[i_b][size_b_index]
        diff_type_penalty = type_penalty * abs(avg_type_a - avg_type_b)

        penalty = (diff_size_penalty 
            + diff_por_penalty 
            + diff_type_penalty
            + diff_h_penalty
        )
        return penalty

    a_len = len(a_types)
    b_len = len(b_types)

    cache_a = np.zeros(a_len*b_len, dtype=int).reshape((a_len, b_len))   
    cache_b = np.zeros(a_len*b_len, dtype=int).reshape((a_len, b_len))   
    cache_ans = np.zeros(a_len*b_len, dtype=float).reshape((a_len, b_len))   
    
    c = cache(cache_a, cache_b, cache_ans)
    
    for a_i in range(a_len):
        for b_i in range(b_len):
            fill_levi(
                a_index = a_i, 
                b_index = b_i, 
                window_sizes = window_sizes,
                compare_penalty_fn = compare_penalty_fn,
                delete_penalty_per_point = delete_penalty_per_point,
                cache = c
            )

    rm_c = 0
    cmp_c = 0

    ans = list()
    current_a = a_len - 1
    current_b = b_len - 1
    while current_a > 0 and current_b > 0:
        next_a = c.a[current_a, current_b]
        next_b = c.b[current_a, current_b]

        if next_a != current_a and next_b != current_b:
            cmp_c += current_a - next_a
            print("cmp" + str(current_a) + ":" + str(current_a - next_a))
            ans.append(((current_a, current_b), (next_a - 1, next_b - 1)))
        else:
            rm_c += current_a + current_b - next_a - next_b
            print("rm: " + str(current_a) + ":" + str(current_a + current_b - next_a - next_b))

        current_a = next_a
        current_b = next_b
    print("")
    print(str(cmp_c))
    print(str(rm_c))
    return ans

def test_trapeziums():
    a_pors = pd.read_excel('./sample_data/WellA.xlsx')
    a_types = pd.read_excel('./sample_data/WellACoreDescription.xlsx')
    b_pors = pd.read_excel('./sample_data/WellB.xlsx')
    b_types = pd.read_excel('./sample_data/WellBCoreDescription.xlsx')
    
    a_types_param = [1 if val == 'sandstone' else 0 for idx, val in enumerate(a_types.values[:,1]) if (idx % 7) % 2 == 0 ]
    a_types_param = a_types_param[:-1]
    b_types_param = [1 if val == 'sandstone' else 0 for idx, val in enumerate(b_types.values[:,1])]
    a_pors_param = list(a_pors.values[:,1])
    b_pors_param = list(b_pors.values[:,1])

    a_types_param = [val for idx, val in enumerate(a_types_param) if idx % 40 == 0]
    b_types_param = [val for idx, val in enumerate(b_types_param) if idx % 40 == 0]
    a_pors_param = [val for idx, val in enumerate(a_pors_param) if idx % 40 == 0]
    b_pors_param = [val for idx, val in enumerate(b_pors_param) if idx % 40 == 0]
    
    while len(a_pors_param) < len(a_types_param):
        idx = random.randint(0, len(a_pors_param) - 2)
        a_pors_param.insert(idx, (a_pors_param[idx] + a_pors_param[idx + 1]) / 2)

    while len(b_pors_param) < len(b_types_param):
        idx = random.randint(0, len(b_pors_param) - 2)
        b_pors_param.insert(idx, (b_pors_param[idx] + b_pors_param[idx + 1]) / 2)

    return ((a_types_param, b_types_param, a_pors_param, b_pors_param), find_trapeziums(
        a_types_param, 
        b_types_param, 
        a_pors_param, 
        b_pors_param, 
    ))
if __name__ == "__main__":
    test_trapeziums()