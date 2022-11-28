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


# 11/28
이번에 구현한 것
- NLD token, NL grammar를 추가하여 new_line handling을 해결한 것 같습니다. 간단한 if, else문에서 줄바꿈의 유무에 따라 parser error의 유무를 확인했습니다.
- 유사 parse_tree 제작. 각 grammar에서 주요한 value들을 재귀적인 튜플 형태로 반환하게 하였습니다. 프로그램을 실행하면 튜플형태의 parse tree를 종류별 stmt가 끝나면 출력합니다.
- print_statement 추가 및 개별 statement의 detail 수정. 실행 해보면서 오류가 나거나, 수정해야겠다 싶은 부분을 수정했습니다.

논외 사항
- switch, if에서의 := 사용 -> ;(semicolon)을 허용하는 문법을 작성해야 해서 많은 수정이 필요할 수 있음
- func의 구현 -> func 내에서 고려해야할 detail이 많고, main함수와 구별하기가 까다로움
- 그 외 나머지 문법 들...

앞으로 구현해야 할 것!
- for_statement -> ++ / -- 를 구현해야 한다..
- global_assign -> global_scope와 main_scope 구분이 필요 / global_scope는 코드 위치에 상관없이 먼저 선언 됨
- 전체적인 점검 및 input 예시 작성
