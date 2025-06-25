#include <iostream>
#include <vector>
#include <queue>
using namespace std;
int ROW, COL;

vector<vector<int>> InputData()
{
    cin >> ROW >> COL;
    vector<vector<int>> data(ROW, vector<int>(COL, 0));
    int temp = 0;
    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COL; j++)
        {
            cin >> temp;
            data[i][j] = temp;
        }
    }
    return data;
}

int toMark = 2;
bool isValid(vector<vector<int>> &data, int x, int y)
{
    if (x - 1 >= 0 && data[x - 1][y] != data[x][y])
    {
        return true;
    }

    if (x + 1 < ROW && data[x + 1][y] != data[x][y])
    {
        return true;
    }

    if (y - 1 >= 0 && data[x][y - 1] != data[x][y])
    {
        return true;
    }

    if (y + 1 < COL && data[x][y + 1] != data[x][y])
    {
        return true;
    }
    return false;
}

void MarkUp(vector<vector<int>> &data, int x, int y)
{
    if (x < 0 || x >= ROW || y < 0 || y >= COL)
    {
        return;
    }

    int c = data[x][y];
    data[x][y] = toMark;
    if (x - 1 >= 0 && data[x - 1][y] == c)
    {
        MarkUp(data, x - 1, y);
    }

    if (x + 1 < ROW && data[x + 1][y] == c)
    {
        MarkUp(data, x + 1, y);
    }

    if (y - 1 >= 0 && data[x][y - 1] == c)
    {
        MarkUp(data, x, y - 1);
    }

    if (y + 1 < COL && data[x][y + 1] == c)
    {
        MarkUp(data, x, y + 1);
    }
}

void bfs(vector<vector<int>> &data, vector<vector<int>> &estimated, int row, int col)
{
    queue<vector<int>> toVisit;
    toVisit.push(vector<int>{row, col, 0});
    while (!toVisit.empty())
    {
        int size = toVisit.size();
        while (size-- > 0)
        {
            vector<int> p = toVisit.front();
            toVisit.pop();
            int x = p[0];
            int y = p[1];
            int l = p[2];

            if (x - 1 >= 0 && data[x - 1][y] != 2 && l + 1 < estimated[x - 1][y])
            {
                estimated[x - 1][y] = l + 1;
                toVisit.push(vector<int>{x - 1, y, l + 1});
            }

            if (x + 1 < ROW && data[x + 1][y] != 2 && l + 1 < estimated[x + 1][y])
            {
                estimated[x + 1][y] = l + 1;
                toVisit.push(vector<int>{x + 1, y, l + 1});
            }

            if (y - 1 >= 0 && data[x][y - 1] != 2 && l + 1 < estimated[x][y - 1])
            {
                estimated[x][y - 1] = l + 1;
                toVisit.push(vector<int>{x, y - 1, l + 1});
            }

            if (y + 1 < COL && data[x][y + 1] != 2 && l + 1 < estimated[x][y + 1])
            {
                estimated[x][y + 1] = l + 1;
                toVisit.push(vector<int>{x, y + 1, l + 1});
            }
        }
    }
}

int solve(vector<vector<int>> &data)
{
    vector<vector<int>> estimated(ROW, vector<int>(COL, INT_MAX));

    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COL; j++)
        {
            if (data[i][j] == 2 && isValid(data, i, j))
            {
                estimated[i][j] = 0;
            }
        }
    }

    int res = INT_MAX;
    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COL; j++)
        {
            if (data[i][j] == 2 && isValid(data, i, j))
            {
                bfs(data, estimated, i, j);
            }
        }
    }

    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COL; j++)
        {
            if (data[i][j] == 3)
            {
                res = min(res, estimated[i][j]);
            }
        }
    }

    return res - 1;
}

int main()
{
    vector<vector<int>> data = InputData();
    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COL; j++)
        {
            if (data[i][j] == 1)
            {
                MarkUp(data, i, j);
                toMark++;
            }
        }
    }

    cout << solve(data) << endl;
    return 0;
}