#include <bits/stdc++.h>
using namespace std;

using ll = long long;

class SpTable {
 public:
    SpTable(vector<ll>& toCompute) : sp(),
                                     n(toCompute.size()) {
        compute(toCompute);
    }

    SpTable(ll maxSize = 0) : maxSize(maxSize), n(maxSize), k(ceil(log2(maxSize)) + 1), sp(k + 1, vector<ll>(n, 0)) {}

    void resize(int size) {
        this->n = size;
        this->k = ceil(log2(size)) + 1;
    }

    void compute(vector<ll>& input) {
        resize(input.size());
        std::copy(input.begin(), input.end(), sp[0]);
        for (ll i = 1; i < sp.size(); i++) {
            for (ll j = 0; j + (1 << i) < n; j++) {
                sp[i][j] = f(sp[i - 1][j], sp[i - 1][j + (1 << (i - 1))]);
            }
        }
    }

    static ll f(ll& lhs, ll& rhs) {
        /** f must be idempotent function - min, max, lcm, gcd */
        return 0;
    }

    ll query_range(ll L, ll R) {
        ll i = log2(R - L + 1);
        return f(sp[i][L], sp[i][R - (1 << i) + 1]);
    }

 public:
    ll maxSize;
    ll n;   // size of original array
    ll k;   // 1st dimension of sp - k >= log2(n)
    vector<vector<ll>> sp;
};