from collections import deque

# 마법의 숲 탐색

# 1. 남쪽 / 2. 서쪽 + 반시계 + 남쪽 / 3. 동쪽 + 시계 + 남쪽
# 골렘 출구와 다른 골렘이 인접하면 다른 골렘으로 이동 가능
# 정령은 가장 남쪽 칸까지 이동
# 골렘이 숲에 진입하지 못하면 리셋

# 입력
# R, C, K : 행, 열, 정령 수
# 출발 열, 출구 정보 (0,1,2,3 = 북,동,남,서)


R, C, K = map(int, input().split())
A = [[0] * 100 for _ in range(100)]  # 3 ~ R+2, 0 ~ C-1 사용 예정, value는 골렘의 id
isExit = [[0] * 100 for _ in range(100)]
answer = 0
dys = [-1, 0, 1, 0]  # 상 하
dxs = [0, 1, 0, -1]  # 좌 우


def resetMap():
    for i in range(R+3):
        for j in range(C):
            A[i][j] = 0
            isExit[i][j] = False

def in_range(r, c):
    return r >= 3 and r < R+3 and c >= 0  and c < C

def canGo(r, c):
    flag = c-1 >= 0 and c+1 < C and r+1 < R+3
    flag = flag and (A[r - 1][c - 1] == 0)
    flag = flag and (A[r - 1][c] == 0)
    flag = flag and (A[r - 1][c + 1] == 0)
    flag = flag and (A[r][c - 1] == 0)
    flag = flag and (A[r][c] == 0)
    flag = flag and (A[r][c + 1] == 0)
    flag = flag and (A[r + 1][c] == 0)
    return flag


def bfs(r, c):
    result = r
    q = deque([(r, c)])
    visit = [[False] * C for _ in range(R+3)]
    visit[r][c] = True

    while q:
        cur_r, cur_c = q.popleft()
        for k in range(4):
            nr, nc = cur_r + dys[k], cur_c + dxs[k]

            if in_range(nr, nc) and not visit[nr][nc] \
                    and (A[nr][nc] == A[cur_r][cur_c] or (A[nr][nc] != 0 and isExit[cur_r][cur_c])):
                q.append((nr, nc))
                visit[nr][nc] = True
                result = max(result, nr)

    return result


def down(r, c, d, id):
    if canGo(r+1, c):
        # 남쪽으로 이동
        down(r+1, c, d, id)
    elif canGo(r+1, c-1):
        # 서 + 남
        down(r+1, c-1, (d+3)%4, id)
    elif canGo(r+1, c+1):
        # 서
        down(r+1, c+1, (d+1)%4, id)
    else:
        if not in_range(r-1, c-1) or not in_range(r+1, c+1):
            resetMap()
        else:
            A[r][c] = id
            for k in range(4):
                A[r+dys[k]][c+dxs[k]] = id
            isExit[r+dys[d]][c+dxs[d]] = True
            global answer
            # print(answer)
            answer += bfs(r, c) - 3 + 1

for id in range(1, K+1):
    c, d = map(int, input().split())
    down(0, c-1, d, id)

print(answer)