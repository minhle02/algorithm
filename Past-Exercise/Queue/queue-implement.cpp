#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <map>
#include <queue>
#include <string>
#include <algorithm>
#include <stdexcept>
using namespace std;

template <typename T> class Queue {
    public:
        Queue() : size(0) {};
        void push(T element) {
            mVtAdd.push_back(element);
            size++;
        }
        void pop() {
            if (size == 0) {
                return;
            }
            if (mVtPop.size() != 0) {
                mVtPop.pop_back();
            } else {
                while (!mVtAdd.empty()) {
                    mVtPop.push_back(mVtAdd.back());
                    mVtAdd.pop_back();
                }
                mVtAdd.clear();
                mVtPop.pop_back();
            }
            size--;
        }
        T front() {
            try {
                if (size == 0) {
                    throw "Error";
                }
                if (mVtAdd.size() != 0) {
                    return mVtAdd.front();
                } else {
                    return mVtPop.back();
                }
            }
            catch (string &w)
            {
                cout << w << endl;
            }
        }
        void print() {
            cout << "Queue content:\n";
            for (auto it = mVtPop.rbegin(); it != mVtPop.rend(); it++) {
                cout << *it << " ";
            }
            for (auto it = mVtAdd.begin(); it != mVtAdd.end(); it++)
            {
                cout << *it << " ";
            }
            cout << endl;
        }

    private:
        vector<T> mVtAdd;
        vector<T> mVtPop;
        int size;
};

int main()
{
    Queue<int> testQueue;
    for (int i = 0; i < 10; i++) {
        testQueue.push(i);
    }
    return 0;
}