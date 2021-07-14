import random
import numpy as np
import time
import copy

distance_matrix = input()

# 초기해 랜덤으로 설정
route = [7, 2, 3, 9, 4, 12, 11, 8, 1, 6, 5, 10]
route = random.sample(route,len(route))

# 새로운 neighbor 추출
def random_dir(list):
        rand_ind = random.randint(0, len(list) - 2)
        new_list = copy.deepcopy(list)  # 새로운 리스트를 만들때 deepcopy를 이용해서 id 새로부여
        a = list[rand_ind]
        b = list[rand_ind + 1]
        new_list[rand_ind] = b
        new_list[rand_ind + 1] = a
        return new_list


# 경로의 거리 추출
def distance(list):
        sum = 0
        for i in range(len(list) - 1):
                sum += distance_matrix[list[i]][list[i + 1]]
        tmp = distance_matrix[0][list[0]] + distance_matrix[list[len(list) - 1]][0]
        sum += tmp
        return sum


# SA 알고리즘
def sa(dir, t_0, t_min, alpha, count):
        start = time.time()
        T = t_0
        dist = distance(dir)
        best_dist = dist
        best_dir = copy.deepcopy(dir)

        while T > t_min:  # 최소온도가 될때까지 반복
                for i in range(count):  # 온도당 반복수
                        new_dir = random_dir(dir)
                        new_dist = distance(new_dir)

                        if new_dist < dist:  # 좋은 해를 발견할 경우
                                dist = new_dist
                                dir = new_dir

                        else:
                                diff = new_dist - dist
                                if np.exp(-(diff / T)) >= np.random.rand():  # 안좋은 해일지라도 다른 지역을 탐색할수 있는 경우
                                        dist = new_dist
                                        dir = new_dir

                        if dist < best_dist:  # 최적해를 발견할 경우
                                best_dist = dist
                                best_dir = dir

                        # 시간단축을 위해 print 주석처리
                        # print("Temperatue: {}, Direction: {}, Distance: {}, Best: {}".format(T,dir,dist,best_dist))
                T = T * alpha

        print(time.time() - start)
        return best_dir, best_dist

best_dir,best_dist = sa(route,1000,0.01,0.9997,80)