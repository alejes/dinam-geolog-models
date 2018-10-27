# import numpy as np
import statistics


class WorkerConfig:
    MAX_HIGN_SIZE = 600


def normalize_one(data, start, end, step):
    if not data:
        return []

    current = start
    index = 0
    values = []
    answer = []
    # print("[[", current, current+step)
    while current < end:
        if index < len(data) and current + step >= data[index][0]:
            # print (current + step, "<=", data[index][0])
            values.append(data[index][1])
            index += 1
        else:
            if not values:
                if index == 0:
                    values.append(data[0][1])
                elif index == len(data):
                    values.append(data[-1][1])
                else:
                    values.append(data[index][1])
            # print(current, values)
            answer.append(statistics.median(values))
            values = []
            if index < len(data) and current + step == data[index][0]:
                values.append(data[index][1])
            current += step
            # print("[[", current, current + step)

    print(answer)

# def normalize_one(data, start, end, step):
#     size = len(data)
#     size += data[0][0] != start
#     size += data[-1][0] != end
#     keys = np.zeros((size,))
#     print(keys)
#     index = 0
#
#     if data[0][0] != start:
#         keys[index] = start
#         index += 1
#
#     for el, _ in data:
#         keys[index] = el
#         index += 1
#
#     if data[-1][0] != end:
#         keys[index] = end
#         index += 1
#     print(keys)
#
#     splited = np.array_split(data, WorkerConfig.MAX_HIGN_SIZE)
#     print(splited)
#         # print(data)


def normalize_rocks(data1, data2):
    start = min(data1[0][0], data2[0][0])
    end = max(data1[-1][0], data2[-1][0])
    step = (end - start) / WorkerConfig.MAX_HIGN_SIZE
    # print(start, end)
    # print(step)
    norm1 = normalize_one(data1, start, end, step)
    norm2 = normalize_one(data1, start, end, step)
    return norm1, norm2


data1 = [[-10, 5], [1, 10], [2, 15], [3, 15], [4, 25], [5, 15]]
data2 = [[1, 10], [2, 15]]



-10 -2.5
-10, 5

normalize_rocks(data1, data2)
