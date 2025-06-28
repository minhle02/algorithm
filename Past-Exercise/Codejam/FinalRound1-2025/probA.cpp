/**
 * Link: https://codejam.lge.com/contest/problem/1520/1
 * 
 */
#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

#define endl "\n"
#define FOR(i, L ,R) for (long long i = L; i < R; i++)
#define FOR0(i, N) for (long long i = 0; i < N; i++)

constexpr int32_t DP_LIM = 1000000007;
#define int long long

#ifdef __DEBUG__
#define PRINT_VECTOR(v) do {cout << "Container " << #v << "\n"; for (auto&e : v) {cout << e << " ";} cout << "\n";} while (false)
#define DEBUG(...) do {printf(__VA_ARGS__);} while (false)
#define DEBUG_COUT std::cout
#else
#define PRINT_VECTOR(v) (void)0
#define DEBUG(...) (void)0
#define DEBUG_COUT if (false) std::cout
#endif

using ll = long long;
using vi = vector<long long>;
using vii = vector<vector<long long>>;


vi D, C, prefixSum;
ll total;

void solve() {
    ll lastPos = D.size() - 1;
    FOR0(i, C.size()) {
        ll c = C[i];
        auto it = upper_bound(D.begin(), D.end(), c);
        auto d = distance(D.begin(), it);
        DEBUG_COUT << "c: " << c << ",d: " << d << " ";
        if (d > lastPos) {
            cout << 0 << "\n";
        } else {
            ll sum = total - prefixSum[d];
            ll numOfEl = (D.size() - d);
            ll logCount = sum - numOfEl * c;
            if (logCount < 0) {
                cout << 0 << endl;
            } else {
                srand((unsigned)time(0));
                ll randomN = (rand() % 2)+1;
                total -= logCount;
                cout << logCount << endl;
                lastPos = d;
            }
        }
    }
}


int32_t main() {
    DEBUG_COUT << "Debug mode is ON" << endl;
#ifdef __FILEIO__
    freopen("input.txt", "r", stdin);
    freopen("output_main.txt", "w", stdout);
#endif
    cin.tie(0);
    cout.tie(0);
    ios_base::sync_with_stdio(0);

    ll N, M;
    cin >> N >> M;

    D.resize(N);
    C.resize(M);
    FOR0(i, N) {
        cin >> D[i];
    }
    prefixSum.resize(N + 1, 0);
    sort(D.begin(), D.end());
    PRINT_VECTOR(D);
    FOR0(i, N) {
        prefixSum[i + 1] = D[i] + prefixSum[i];
    }
    PRINT_VECTOR(prefixSum);
    total = prefixSum.back();

    FOR0(i, M) {
        cin >> C[i];
        C[i] = C[i] - i;
    }
    PRINT_VECTOR(C);
    solve();

    return 0;
}
