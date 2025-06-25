#include <bits/stdc++.h>
using namespace std;

using ll = long long;
class DSU {
 public:
    DSU(int n) : parent(n, -1), size(n, 0), count(n) {}

    void make_set(ll v) {
        parent[v] = v;
        size[v] = 1;
    }

    int find_set(int v) {
        if (parent[v] == -1) {
            make_set(v);
            return v;
        } else if (parent[v] == v) {
            return v;
        }
        return parent[v] = find_set(parent[v]);
    }

    void union_sets(int a, int b) {
        a = find_set(a);
        b = find_set(b);
        if (a != b) {
            if (size[a] >= size[b]) {
                parent[b] = a;
                size[a] += size[b];
            } else {
                parent[a] = b;
                size[b] += size[a];
            }
            count--;
        }
    }

    int get_count() {
        return count;
    }
 private:
    vector<ll> parent;
    vector<ll> size;
    int count;
};