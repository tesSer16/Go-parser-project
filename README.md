# Go-parser-project

#<11-20>
결론적으로, 이번에 구현하기로 했었던 연산자들에 대해서 대부분 구현하는데 성공한 것 같습니다.

우선 데이터 타입을 int와 bool로 한정했고, 
int op에 대해는 expression을 grammer의 variable로 사용했으며 bool op에는 condition을 사용했습니다.

할당 연산자 '='에 대하여 var a = 3, var a int = 3을 모두 허용하도록 구현했으며,
뒤에 타입 keyword가 있을 경우에는 type check를 하도록 임시로 조치해놓았습니다.

현재는 python shell같이 구현을 해놓아서 입력한 stmt의 value를 반환하지만, 
추후에 parse 구조를 반환하게 바꾸는 등의 방법을 사용할 수 있을 것 같습니다.


어제 주신 코드에서의 이슈에 대해서도 생각해 보았는데,
lex에 관해서는 prefix가 문제가 된 것으로 보입니다. 
ply 공식 document(http://www.dabeaz.com/ply/ply.html)를 조금 읽어보니 token의 선언 순서가 길이가 긴 것 부터 되지 않으면
예를 들어, '+' 와 '+='을 구분할 때 항상 '+'로 구분하게 된다고 하네요...
저도 코드 작성해보면서 이런 형태의 오류가 자주 나왔던 것 같습니다.

parser에서는 우선 grammer를 선언할 때 colon 대신 화살표를 쓴게 분제 될 수 도 있을 것 같습니다.
그리고 말씀하신 p sequence에 type을 따로따로 assign하는 것에 대하여 
저는 앞서 말씀드린 variable을 분리하는 방식을 사용했습니다.

grammer는 임시로 짠거라서 precedence나 conflict에 대해서 아직 검증하지는 않았습니다.
이 문제는 추후에 또 논의해 보면 좋을 것 같습니다.
