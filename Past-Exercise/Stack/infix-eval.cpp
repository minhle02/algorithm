#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <map>
#include <set>
#include <queue>
#include <string>
#include <algorithm>
using namespace std;

vector<string> InfixToPostfix(string s)
{
    string temp = "";
    vector<string> res;
    stack<char> st;
    for (int i = 0; i < s.size(); i++)
    {
        if (s[i] == ' ')
        {
            continue;
        }
        if (s[i] >= '0' && s[i] < '9')
        {
            temp += s[i];
            continue;
        }
        if (temp != "")
        {
            res.push_back(temp);
            temp = "";
        }

        switch (s[i])
        {
        case '(':
        case '+':
        case '-':
        {
            while (!st.empty() && st.top() != '(')
            {
                cout << st.top() << endl;
                char t[2] = {st.top(), '\0'};
                res.push_back(t);
                st.pop();
            }
            st.push(s[i]);
            break;
        }
        case ')':
        {
            while (!st.empty() && st.top() != '(')
            {
                string t = "";
                res.push_back(t + st.top());
                st.pop();
            }
            st.pop();
            break;
        }
        }
    }
    if (temp != "")
    {
        res.push_back(temp);
    }
    while (!st.empty())
    {
        string t = "";
        res.push_back(t + st.top());
        st.pop();
    }
    return res;
}
int calculate(string s)
{
    vector<string> temp = InfixToPostfix(s);
    // for (string i : temp) {
    //     cout << i << " ";
    // }
    // cout << endl;
    stack<int> eval;
    for (string i : temp)
    {
        switch (i[0])
        {
        case '+':
        {
            int num1 = eval.top();
            eval.pop();
            int num2 = eval.top();
            eval.pop();
            eval.push(num1 + num2);
            break;
        }
        case '-':
        {
            int num2 = eval.top();
            eval.pop();
            int num1 = eval.top();
            eval.pop();
            eval.push(num1 - num2);
            break;
        }
        default:
        {
            eval.push(stoi(i));
            break;
        }
        }
    }
    return eval.top();
}
int main(int argc, char const *argv[])
{
    string s = "(1+(4+5+2)-3)+(6+8)";
    cout << calculate(s) << endl;
    return 0;
}
