# Go-parser-project

# 11/25
이번에 구현한 것
- const assign 추가 및 redeclared check 추가
- 할당 연산자 +=, -=, *=, /=, %= 및 :=
- 재할당에 대하여 const, type check 추가
- 할당시 default value check
- /, % 연산 시 zero-division check
- string type 구현 및 expr 연산 시 string check 추가
- condition EQ, NE 추가

임시 수정 사항
- import_statement, is_fmt를 추가하여 import를 강제하지 않았습니다.
- 그에 맞게 statement, start 구조를 수정하였습니다.
- 일부 var이나 함수명을 변경하였습니다.
- file execution과 interactive mode를 만들어 놓긴 했는데 file test를 해보지는 않았습니다. interective는 assign의 디버깅 용이고, 후에는 file로 디버깅을 하게 될 것 같습니다.
- switch의 def 있는 경우를 일단 제외하였습니다.

논의가 필요한 사항
1. else 등의 blank 처리
2. global 처리를 확장한 scope 처리: 현재 scope를 tracking하여 그 스코프에서 선언되는 것들을 스코프 인식을 통해 처리하면 어떨까합니다. 물론 이 경우에도 global은 따로 처리가 돼야하긴 합니다.
3. 함수, switch등에서의 detail 및 이슈
- switch, if에서 :=의 사용(block scope)
- 함수 parameter 및 ',' 사용 시 
4. 함수 밖에서는 non-declare statement가 불가(go 문법)
5. break, continue, etc.
6. ++ / --
7. func 안에 func 불가
