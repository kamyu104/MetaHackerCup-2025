# Copyright (c) 2025 kamyu. All rights reserved.
#
# Meta Hacker Cup 2025 Round 3 - Problem D. Treehouse Telegram
# https://www.facebook.com/codingcompetitions/hacker-cup/2025/round-3/problems/D
#
# Time:  O(N * (logN)^2)
# Space: O(N)
#

def treehouse_telegram():
    def build_hld(adj):
        parent, depth, size, heavy, head, pos = [-1]*len(adj), [0]*len(adj), [1]*len(adj), [-1]*len(adj), list(range(len(adj))), [-1]*len(adj)
        stk = [(1, 0, -1)]
        while stk:
            step, u, p = stk.pop()
            if step == 1:
                parent[u], depth[u] = p, (depth[p]+1 if p != -1 else 0)
                stk.append((2, u, p))
                for v in adj[u]:
                    if v == p:
                        continue
                    stk.append((1, v, u))
            elif step == 2:
                for v in adj[u]:
                    if v == parent[u]:
                        continue
                    size[u] += size[v]
                    if heavy[u] == -1 or size[v] > size[heavy[u]]:
                        heavy[u] = v
        idx = 0
        stk = [(0, 0)]
        while stk:
            u, h = stk.pop()
            head[u], pos[u] = h, idx
            idx += 1
            for v in adj[u]:
                if v == parent[u] or v == heavy[u]:
                    continue
                stk.append((v, v))
            if heavy[u] != -1:
                stk.append((heavy[u], h))
        return parent, depth, head, pos

    def lca(u, v):
        while head[u] != head[v]:
            if depth[head[u]] < depth[head[v]]:
                u, v = v, u
            u = parent[head[u]]
        return u if depth[u] < depth[v] else v

    def compress_tree(nodes):
        nodes.sort(key=lambda x: pos[x])
        vals = sorted(set(nodes+[lca(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]), key=lambda x: pos[x])
        val_to_idx = {u:i for i, u in enumerate(vals)}
        edges = []
        for i in range(1, len(vals)):
            j = lca(vals[i-1], vals[i])
            edges.append((i, val_to_idx[j], depth[vals[i]]-depth[j]))
        return val_to_idx, edges

    N = int(input())
    A_B = [list(map(int, input().split())) for _ in range(N-1)]
    adj = [[] for _ in range(N)]
    for A, B in A_B:
        adj[A-1].append(B-1)
        adj[B-1].append(A-1)
    parent, depth, head, pos = build_hld(adj)
    f = [0]*(N+1)
    for d in range(1, N+1):
        nodes = list(range(d-1, N, d))
        if len(nodes) <= 1:
            continue
        val_to_idx, edges = compress_tree(nodes)
        cnt = [0]*len(val_to_idx)
        for u in nodes:
            cnt[val_to_idx[u]] = 1
        for c, p, _ in reversed(edges):
            cnt[p] += cnt[c]
        f[d] = sum(l*cnt[c]*(len(nodes)-cnt[c]) for c, _, l in edges)
    for d in reversed(range(1, N+1)):
        for k in range(2*d, N+1, d):
            f[d] -= f[k]
    return " ".join(map(str, (f[i] for i in range(1, N+1))))

for case in range(int(input())):
    print('Case #%d: %s' % (case+1, treehouse_telegram()))
