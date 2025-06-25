#include <bits/stdc++.h>
using namespace std;

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

int32_t main() {
    DEBUG_COUT << "Debug mode is ON" << endl;
#ifdef LOCALONLY
    freopen("$input", "r", stdin);
    freopen("$output", "w", stdout);
#endif
    cin.tie(0);
    cout.tie(0);
    ios_base::sync_with_stdio(0);
    cout << "Hello, World!" << endl;
    return 0;
}
