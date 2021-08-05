import pandas as pd
import random
import numpy as np
import time
import copy
import math

class SA():
    def __init__(self,data,dire,t_0,t_min,alpha, count, cutoffTime):
        self.data = data
        self.dire = dire
        self.t_0 = t_0
        self.t_min = t_min
        self.alpha = alpha
        self.count = count
        self.cutoffTime = cutoffTime
        # 유클리드 거리 행렬
        result = []
        for i in self.data:
            for j in self.data:
                tmp = np.sqrt(np.sum(np.square(np.array(i)-np.array(j))))
                result.append(tmp)
        result = np.array(result)
        result = np.reshape(result, (len(self.data), len(self.data)))
        self.df = pd.DataFrame(result)

    # 경로의 거리 계산
    def r_distance(self,route):
        self.route = route
        sum = 0
        for i in range(len(self.route) - 1):
            sum += self.df[self.route[i]][self.route[i + 1]]
        tmp = self.df[0][self.route[0]] + self.df[self.route[len(self.route) - 1]][0]
        sum += tmp
        return sum

    # 새로운 neighbor 추출
    def random_dir(self,lists, T):
        self.lists = lists
        self.T = T
        new_list = copy.copy(self.lists)
        if self.T > self.t_0 * 0.5:
            rand_ind = random.choices(list(range(98)), k=10)
            for i in range(len(rand_ind) - 1):
                new_list[int(rand_ind[i])], new_list[int(rand_ind[i + 1])] = new_list[int(rand_ind[i + 1])], new_list[
                    int(rand_ind[i])]
        elif self.T > self.t_0 * 0.2:
            rand_ind = random.choices(list(range(99)), k=4)
            for j in range(len(rand_ind) - 1):
                new_list[int(rand_ind[j])], new_list[int(rand_ind[j + 1])] = new_list[int(rand_ind[j + 1])], new_list[
                    int(rand_ind[j])]
        else:
            rand_ind = random.randint(0, len(lists) - 2)
            new_list[rand_ind], new_list[rand_ind + 1] = new_list[rand_ind + 1], new_list[rand_ind]
        return new_list

    # SA 알고리즘
    def sa(self):
        start = time.time()
        T = self.t_0
        dist = self.r_distance(self.dire)
        direc = self.dire
        best_dist = dist
        best_dir = self.dire

        while T > self.t_min:  # 최소온도가 될때까지 반복
            for i in range(self.count):  # 온도당 반복수
                new_dir = self.random_dir(direc, T)
                new_dist = self.r_distance(new_dir)

                if new_dist < dist:  # 좋은 해를 발견할 경우
                    dist = new_dist
                    direc = new_dir
                else:
                    diff = new_dist - dist
                    if math.exp((-diff * 400) / T) >= random.random():  # 안좋은 해일지라도 다른 지역을 탐색할수 있는 경우
                        dist = new_dist
                        direc = new_dir
                if dist < best_dist:  # 최적해를 발견할 경우
                    best_dist = dist
                    best_dir = direc
                    print("T: {}, Dir: {}, Dist:{}, Best:{}".format(T, direc, dist, best_dist))
            T = T * self.alpha

            if (time.time() - start) > self.cutoffTime:
                print(T)
                break
        return best_dir, best_dist