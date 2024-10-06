from collections import deque

# K : 탐사 반복 횟수, M : 벽면에 적힌 유물 조각 개수
K, M = map(int, input().split())

LEN = 5
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

grid = [
    list(map(int, input().split()))
    for _ in range(LEN)
]
next_num = deque(list(map(int, input().split())))

# 격자 회전 함수 90도, 180도, 270도 (3 * 3)
def rotate(input_grid, deg, r, c):
    test = [
        row[:]
        for row in input_grid
    ]
    if deg == 90:
        test[r - 1][c - 1] = input_grid[r + 1][c - 1]
        test[r - 1][c] = input_grid[r][c - 1]
        test[r - 1][c + 1] = input_grid[r - 1][c - 1]
        test[r][c + 1] = input_grid[r - 1][c]
        test[r + 1][c + 1] = input_grid[r - 1][c + 1]
        test[r + 1][c] = input_grid[r][c + 1]
        test[r + 1][c - 1] = input_grid[r + 1][c + 1]
        test[r][c - 1] = input_grid[r + 1][c]
    elif deg == 180:
        test[r - 1][c - 1] = input_grid[r + 1][c + 1]
        test[r - 1][c] = input_grid[r + 1][c]
        test[r - 1][c + 1] = input_grid[r + 1][c - 1]
        test[r][c + 1] = input_grid[r][c - 1]
        test[r + 1][c + 1] = input_grid[r - 1][c - 1]
        test[r + 1][c] = input_grid[r - 1][c]
        test[r + 1][c - 1] = input_grid[r - 1][c + 1]
        test[r][c - 1] = input_grid[r][c + 1]
    elif deg == 270:
        test[r - 1][c - 1] = input_grid[r - 1][c + 1]
        test[r - 1][c] = input_grid[r][c + 1]
        test[r - 1][c + 1] = input_grid[r + 1][c + 1]
        test[r][c + 1] = input_grid[r + 1][c]
        test[r + 1][c + 1] = input_grid[r + 1][c - 1]
        test[r + 1][c] = input_grid[r][c - 1]
        test[r + 1][c - 1] = input_grid[r - 1][c - 1]
        test[r][c - 1] = input_grid[r - 1][c]

    return test

def in_range(i, j):
    return i >=0 and i < LEN and j >= 0 and j < LEN



def get(input_grid):
    test = [
        row[:]
        for row in input_grid
    ]
    visited = [[0] * LEN for _ in range(LEN)]
    d = deque([])
    result = []

    for i in range(LEN):
        for j in range(LEN):
            if visited[i][j]:
                continue
            else:
                temp = []
                d.append((i, j))
                visited[i][j] = True
                while d:
                    cur_i, cur_j = d.popleft()
                    temp.append((cur_i, cur_j))
                    for k in range(4):
                        next_i, next_j = cur_i + dr[k], cur_j + dc[k]
                        if in_range(next_i, next_j) and not visited[next_i][next_j] and test[next_i][next_j] == test[i][j]:
                            d.append((next_i, next_j))
                            visited[next_i][next_j] = True

                result.append(temp)

    # print(result)
    return result





# 1. 가치 최대화 / 2. 각도 최소화 / 3. 열 최소화 / 4. 행 최소화

# 유물 3개 이상 연결 -> 유물이 되어 사라짐, 가치 = 연결된 유물 조각 개수 (DFS? BFS?)
# 먼저 돌리고, 가치 구해보고, 열, 행 저장
# 위의 기준에 맞는 걸 선택후 grid에 저장

# 유물 조각 채우는 함수
# 1. 열이 작은거 부터 / 2. 행이 큰거 부터 (죄측 하단부터 채움)
# 유물 채우고 다시 유물 획득 필요

# K번 반복
# 유물 획득 불가능하면 탐사 종료

## main code
score = 0
test = [
        row[:]
        for row in grid
    ]
for _ in range(K):
    max_get = 0
    rotate_i, rotate_j, degree = 0, 0, 0
    for i in range(1, 4):
        for j in range(1, 4):
            # 270도 회전
            result_270 = get(rotate(test, 270, i, j))
            get_270 = 0
            for item in result_270:
                if len(item) >= 3:
                    get_270 += len(item)

            if get_270 > max_get:
                max_get = get_270
                rotate_i, rotate_j, degree = i, j, 270
            elif get_270 == max_get:
                if degree == 270:
                    if j < rotate_j:
                        rotate_i, rotate_j, degree = i, j, 270
                    elif j == rotate_j and i < rotate_i:
                        rotate_i, rotate_j, degree = i, j, 270
                elif degree > 270:
                    rotate_i, rotate_j, degree = i, j, 270

    for i in range(1, 4):
        for j in range(1, 4):
            # 180도 회전
            result_180 = get(rotate(test, 180, i, j))
            get_180 = 0
            for item in result_180:
                if len(item) >= 3:
                    get_180 += len(item)

            if get_180 > max_get:
                max_get = get_180
                rotate_i, rotate_j, degree = i, j, 180
            elif get_180 == max_get:
                if degree == 180:
                    if j < rotate_j:
                        rotate_i, rotate_j, degree = i, j, 180
                    elif j == rotate_j and i < rotate_i:
                        rotate_i, rotate_j, degree = i, j, 180
                elif degree > 180:
                    rotate_i, rotate_j, degree = i, j, 180

    for i in range(1, 4):
        for j in range(1, 4):
            # 90도 회전
            # if i == 1 and j == 1:
            #     print()
            #     for row in test:
            #         print(row)
            #     print()
            #     for row in rotate(test, 90, i, j):
            #         print(row)

            result_90 = get(rotate(test, 90, i, j))
            get_90 = 0
            for item in result_90:
                if len(item) >= 3:
                    get_90 += len(item)

            if get_90 > max_get:
                max_get = get_90
                rotate_i, rotate_j, degree = i, j, 90
            elif get_90 == max_get:
                if degree == 90:
                    if j < rotate_j:
                        rotate_i, rotate_j, degree = i, j, 90
                    elif j == rotate_j and i < rotate_i:
                        rotate_i, rotate_j, degree = i, j, 90
                elif degree > 90:
                    rotate_i, rotate_j, degree = i, j, 90


    #         print(result_90)
    #
    # print()
    # print(degree, rotate_i, rotate_j)
    # print(max_get)
    if max_get == 0:
        break

    test = rotate(test, degree, rotate_i, rotate_j)


    # 채우고. 검사.
    while True:
        result = get(test)
        count = 0
        for item in result:
            if len(item) >= 3:
                count += len(item)
                for i in item:
                    test[i[0]][i[1]] = 0

        # print(count)

        if count < 3:
            break
        else:
            # 채우기
            score += count
            for j in range(5):
                for i in range(4, -1, -1):
                    if test[i][j] == 0:
                        # print(i, j)
                        test[i][j] = next_num.popleft()


    # for row in test:
    #     print(row)
    if score != 0:
        print(score, end=' ')
    score = 0

print()