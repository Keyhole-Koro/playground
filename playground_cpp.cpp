#include <iostream>
#include <string>
 
using namespace std;
 
int main(){
    string s;
    s = "This is a";
    s.append(" pen.");
    cout << s << endl;
    cout << "length of letters：" << s.length() << endl;
    //  printfで表示
    printf("char*:%s\n",s.c_str());
    return 0;
}