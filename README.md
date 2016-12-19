# Popcorn project API Document

##[gitbook에서 Document 자세히 보기](https://pop-api.gitbooks.io/popcorn-api/content/)

#### 개요

영화 평가 서비스 프로젝트로 다음 영화 API와 크롤링을 활용하여 DB를 구축합니다. 각 영화는 유저가 평가할 수 있으며 평가 데이터로 각 유저에게 맞춤 영화를 추천합니다.

Web, iOS 클라이언트 대상으로 API를 제공합니다.

#### 개발환경
1. python 3.4.3
2. django 1.10.3

#### 서버환경
1. AWS EB
2. RDS Postgres
3. S3 storage

#### ERD(entity-relationship diagram)
![Image of ERD](/assets/erd.png)

#### ERD 요약
![Image of ERD Summery](/assets/erd_summery.png)