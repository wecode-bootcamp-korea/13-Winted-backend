# 13-Winted-backend
## 🌃 프로젝트 소개
>**원티드(Wanted)**는 원티드랩이라는 스타트업에서 운영중인 채용 플랫폼입니다. 2015년부터 서비스하기 시작했습니다. 
특징은 추천이라는 기능이 있어 지원할 때 지인의 추천/추천사를 함께 붙일 수 있고, 합격한 경우 합격자와 추천인에게 50만원 이상의 보상금을 지급해주는 시스템이 있습니다. 
이름있는 기업은 물론 생소한 스타트업이나 소규모 IT기업들도 공고를 많이 올리는 편으로 2019년 기준 4000여개의 기업이 이용하고 있다고 합니다.
이용 기업들과 비슷하게 IT직군 인재풀이 좋은 편이고 개발자는 물론 디자이너, 마케터 그 외 비즈니스 직군과 게임관련 직군들도 폭넓게 있습니다. 

## 🌃 프로젝트 참가자(Front + Back)
### 🏆 Team Winted
![](https://images.velog.io/images/kho5420/post/2d96a779-38e4-45b6-85c9-84bbc1c43122/image.png)
### 👩‍👧‍👧‍👧 FrontEnd
+ 김수연
+ 민지연
+ 김한나
+ 이예린
### 👨‍👨‍ BackEnd
+ 김형욱
+ 박재용

## 🌃 프로젝트 기간
**2020.11.02 ~ 2020.11.13** 약 2주간 진행

## 🌃 프로젝트 영상
## 🌃 기술 스택
### 👩‍👧‍👧‍👧 FrontEnd
+ HTML/CSS
+ JavaScript(ES6),
+ React
+ React-Redux
+ React-Hooks
+ React-router
+ SCSS
+ Styled Component
+ Chart.js
### 👨‍👨‍ BackEnd
+ Python
+ Django
+ CORS Header
+ Bcrypt
+ PyJWT
+ MySQL
+ REST API
+ AqueryTool (데이터베이스 모델링)
### 👫 협업 도구
+ Slack
+ Git + GitHub ([Front](https://github.com/wecode-bootcamp-korea/13-Winted-frontend), [Back](https://github.com/wecode-bootcamp-korea/13-Winted-backend))
+ [Trello](https://trello.com/b/k7IalrMk/winted)를 이용해 일정관리 및 작업 현황 확인
+ Postman (API 관리)

## 🌃 구현한 기능
### 👩‍👧‍👧‍👧 FrontEnd
### 회원가입 & 로그인
+ Winted 로그인,회원가입 및 KaKao API를 활용한 소셜 로그인
+ 로그인, 로그아웃 profile image 변경 구현
### 직군별 연봉 페이지
+ Chart.js 라이브러리를 이용한 직업-연차별 차트 구현
### Nav
+ Nav Dropdown 기능 구현
### 구직정보 리스트 탐색 페이지
+ 구직 정보 카테고리 메뉴 슬라이드 기능 구현
+ 구직 정보 필터링을 위한 모달창 기능 구현
+ 구직 정보 필터링 기능 구현
### 구직정보 상세 페이지
+ Slick을 이용한 기업 소개 이미지 구현
+ Google Map을 이용한 기업 위치 지도 구현
+ 해당 구직정보 좋아요 기능 구현
### 이력서 관리 페이지
+ 이력서 작성 및 저장 기능
### 회원 추천 페이지
+ 추천 페이지 메뉴탭 구현
+ 각각의 component에 따른 모달창 구현
+ 추천사 모달창 수정 및 저장 기능 구현
### 👨‍👨‍ BackEnd
### 회원가입 & 로그인
+ bcrypt를 사용한 암호화
+ JWT 로그인 구현 및 decorator를 이용해서 인증
+ KaKao API를 활용한 소셜 로그인
### 유저 정보
+ 유저별로 탐색페이지 필터 (등록, 조회, 삭제)
+ 유저가 좋아요한 구직정보 (등록, 조회, 삭제)
### Nav
+ 메인, 서브 카테고리 조회 기능
### 구직정보 리스트 탐색 페이지
+ 필터, 정렬, 페이지네이션에 따른 탐색 페이지 조회 기능 (회원/비회원)
### 구직정보 상세 페이지
+ 구직정보 상세페이지 조회 기능
### 직군별 연봉 페이지
+ 직업-연차별 연봉 조회 기능
### 이력서 관리 페이지
+ 회원 이력서 (등록, 조회, 수정, 삭제)
+ 경력, 학력, 수상내역, 외국어능력 (등록, 조회, 수정, 삭제)
### 회원 추천 페이지
+ 회원 추천하기 기능
+ 내가 한 추천, 내가 받은 추천(조회, 삭제)
+ 내가 추천한 회원의 추천사 수정

## 🌃 프로젝트 진행과정
1차 프로젝트와 마찬가지로 Trello를 이용해서 정보 공유 및 작업 현황을 확인했습니다.
Backlog에 처음 기획한 기능들을
Design에는 프로젝트에 필요한 이미지들
To Do(This Week)에는 이번주까지 할 작업들
Doing에는 현재 하고있는 작업들
Testing에는 FrontEnd와 BackEnd간의 테스트 중인 부분들
Done에는 위의 작업들을 완료했을때 작성했습니다.
