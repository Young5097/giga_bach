# giga_bach

## 12월 6일
 + https://dashboard.ngrok.com/get-started/setup
  - ssh colab gpu local연결 키 가져오는 사이트

## 12월 1일
 + 사용자에게 입력을 받는 부분 
  - midi 파일 여부 
   - O : midi_catcher.py로 미디 검출 후 검출된 미디를 getmusic의 입력으로 쓸 수 있게 하기, 입력된 미디 파일은 바로 got_temp_midi 폴더에 담기
   - X : 휘파람, 흥얼거림의 mp3 파일이므로 이를 midi 파일로 바꿔주는 sound_to_midi.py를 돌린 후 
   got_temp_midi폴더에 담기
+ got_temp_midi 경로를 읽어서 getmusic을 돌아 temp_getmusic에 getmusic으로 생성된 임시 미디 폴더에 담기
+ temp_getmusic에서 미디 파일을 읽어들여서 museforme돌기
+ museforemr에서 final_midi폴더에 생성되게끔 하기
+ 시간여부
 - X : 바로 final_midi_to_wav.py를 돌아 wav 파일을 웹에서 재생하게
 - O : 가사생성 api 따오기 + SVS를 통해 노래 불러주기

## 11월 21일
+피치 검출기 추가/음원 추출기 추가
+midiutil 업데이트로 인한 버전 수정

## 11월 20일
+ 게시판 생성/수정/삭제 기능 추가
+ 디자인을 위한 부분화
+ 게시판 마무리 해야함

## 11월 17일
+ 마이페이지 제작 완료, 음원/보컬 생성 페이지 제작 시작
+ 음원/보컬 생성 페이지와 게시판 제작 해야함
+ 비번찾기 기능 만들어야 함

## 11월 16일
+ 회원가입 기능 마무리, 아이디찾기 제작
+ 비번찾기 기능 제작(어려움), 마이페이지 제작 해야함

## 11월 15일
+ 메인페이지, 로그인, 회원가입 제작
+ 메인페이지 꾸밈
+ 로그인, 회원가입 꾸미기 제작 해야함
+ 아이디, 비밀번호 찾기 기능 제작 해야함

## 11월 14일
+ 작업 환경 설정
