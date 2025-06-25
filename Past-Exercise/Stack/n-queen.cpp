#include <vector>
#include <stack>
#include <iostream>
using namespace std;

vector<vector<int>> result;

// bool isSafe(const vector<vector<int>>& board, int row, int col) {
//     int N = board.size();
//     int i, j;
//     for (i = 0; i < N; i++)
//     {
//         if (board[row][i] == 1)
//             return false;
//     }
//     for (i = 0; i < N; i++) {
//         if ( board[i][col] == 1)
//             return false;
//     }
//     for (i = row, j = col; i >= 0 && j >= 0; i--, j--) {
//         if (board[i][j] == 1)
//             return false;
//     }
//     // for (i = row + 1, j = col + 1; i < N && j < N; i++, j++) {
//     //     if (board[i][j] == 1)
//     //         return false;
//     // }
//     for (i = row, j = col; i < N && j >= 0; i++, j--) {
//         if (board[i][j] == 1)
//             return false;
//     }
//     // for (i = row - 1, j = col + 1; i >= 0 && j < N; i--, j++) {
//     //     if (board[i][j] == 1)
//     //         return false;
//     // }
//     return true;
// }

bool isSafe(vector<vector<int>> board,
            int row, int col)
{
    int i, j;
    int N = board.size();

    /* Check this row on left side */
    for (i = 0; i < col; i++)
        if (board[row][i])
            return false;

    /* Check upper diagonal on left side */
    for (i = row, j = col; i >= 0 && j >= 0; i--, j--)
        if (board[i][j])
            return false;

    /* Check lower diagonal on left side */
    for (i = row, j = col; j >= 0 && i < N; i++, j--)
        if (board[i][j])
            return false;

    return true;
}

bool solveNUntil(vector<vector<int>> &board, int col) {
    int N = board.size();
    if (col == N)
    {
        vector<int> correctCol;
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++) {
                if (board[i][j] == 1)
                    correctCol.push_back(j + 1);
            }
        }
        result.push_back(correctCol);
        return true;
    }
    bool res = false;
    for (int i = 0; i < N; i++)
    {
        if (isSafe(board, i, col)) {
            board[i][col] = 1;
            res = solveNUntil(board, col + 1);
            board[i][col] = 0;
        }
    }
    return res;
}

void printAllSolution(int n) {
    result.clear();
    vector<vector<int>> board(n, vector<int>(n, 0));
    if (!solveNUntil(board,0))
        return;
    sort(result.begin(), result.end());
}

// int main(int argc, char const *argv[])
// {
//     printAllSolution(4);
//     cout << "Hihi" << endl;
//     for (auto el : result)
//     {
//         cout << "[ ";
//         for (int i : el)
//         {
//             cout << i << " ";
//         }
//         cout << "]\n";
//     }
//     return 0;
// }
