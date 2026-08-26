# GDI Country Studies Agent: 하위 스킬 입출력 계약표

## 1. 적용 범위

여기서 **하위 스킬**은 별도 런타임 에이전트가 아니라, 현재 `SKILL.md`의 작업 패턴을 분리해 부르는 기능 계약이다. 모든 계약은 `AGENTS.md`의 정본·증거·품질 규칙을 상속한다. 표의 출력은 독자용 HTML이 아니라 작업 결과물이며, 독자용 변경이 필요할 때는 정본 Markdown과 빌드 파이프라인을 통해서만 반영한다.

### 공통 필수 입력

| 필드 | 의미 |
|---|---|
| `country_code` | 대상 ISO3. 국가가 정해지지 않은 설계·교육 요청은 `N/A`를 명시한다. |
| `task_scope` | 진단, 설계, 수집, 수정, 감사, 빌드 중 무엇을 수행하는지와 대상 장·절·파일. |
| `requested_change` | 읽기 전용 검토인지, 정본 수정·생성물 재빌드까지 허용되는지. |
| `evidence_state` | 현재 출처·수치·인용의 검증 상태 및 알 수 없는 공백. |

### 공통 반환 봉투

각 하위 스킬은 다음을 반환하거나 작업 파일에 기록한다: `status`, `scope_checked`, `outputs`, `files_changed`, `verification`, `open_risks`, `handoff_to`. `status`는 검증 상태 어휘를 사용하고, 보고서 준비도는 `structured first-pass`, `deep draft`, `publication candidate`만 사용한다.

## 2. 입출력 계약표

| ID · 하위 스킬 | 트리거와 필수 입력 | 정본 입력·필수 참조 | 계약된 출력 | 허용 변경 / 금지 | 종료 검증·다음 인계 |
|---|---|---|---|---|---|
| S01 구조 진단 | “무엇이 빠졌나?”, 새 국가·장 시작, 폴더 점검. `country_code`, 폴더 목록, 대상 범위 | `[ISO3]/`, `sources/sections/`, `report/`, `raw/`, `processed/`, `code/`; `report_structure.md` | 구조 진단, 누락 파일·장, 고위험 장(3·5·7·16·17) 목록, 우선순위 | 진단은 읽기 전용. 사용자가 허용하면 계획 파일만 갱신 | 1–19장·정본/생성물 관계 확인 → S02, S03, S04 또는 S12 |
| S02 목차·국가특수 쟁점 | 목차 설계, 특별 절 추가·이동·감사. 국가 맥락, 반복 쟁점, 대상 장 | 장·절 원고, 증거계획; `report_structure.md`, `country_specific_issue_protocol.md` | Country-Specific Issue Plan: 쟁점, 중심 주장, 배치 근거, 증거계획, 장 17 연결 | `section_evidence_plan.csv`와 정본 Markdown의 절 제목·배치 수정 가능. 새 최상위 장 남발, 근거 없는 특별 절 금지 | 표준 1–19장 보존, 쟁점당 최소 2개 근거유형 계획 → S03/S04/S07 |
| S03 출처 감사 | 인용·근거·출처 공백, BTI/V-Dem/QoG 사용 검토 | 원고, `source_register.csv`, APA 레지스터, 로컬 문서; `source_quality_rules.md`, `citation_reference_integrity.md`, `output_templates.md` | Claim-Evidence-Source Table 또는 Source Gap Table, 출처별 검증 상태 | 레지스터·근거계획 갱신 가능. 확인 불가 자료를 인용으로 승격하거나 뉴스를 구조적 사실 근거로 쓰는 일 금지 | 공식/국제/학술 출처의 역할 분리, 공백 표시 → S04, S05, S12 |
| S04 스키마·레지스터 관리 | 소스·APA·통계·증거계획 파일 생성·수리·표준화 | `source_register.csv`, `apa_reference_register.json`, `statistical_metadata.csv`, `section_evidence_plan.csv`; `reference_schemas.md` | 스키마 적합 레코드, 안정적 `source_id`·`reference_id`·`indicator_id`·`chart_id` 연결 | 레지스터 파일만 수정. 레지스터가 본문 근거를 대신하는 것, 미검증 레코드를 `verified`로 표기하는 것 금지 | 필수 열·식별자·검증 상태 확인 → S03/S05/S07/S12 |
| S05 인용·참고문헌 및 렌더 링크 | APA 추가·수정·감사, 참고문헌 URL/링크 결함 | `sources/sections/*.md`, `19-01-references.md`, APA·소스 레지스터, 빌더; `citation_reference_integrity.md` | APA Citation Audit Table, 링크 결함 목록 또는 정본 파이프라인 수정 | 원고·참고문헌·레지스터·빌더 수정 가능. 생성 HTML만의 영구 수정, 가짜 DOI/URL, 본문 손실을 금지 | 인용→참고문헌→실재 출처→레지스터→HTML 앵커 5연결 확인; `audit_citations.py`, 필요시 `audit_reference_links.py` → S12 |
| S06 통계 수집·처리·시각화 | 추세·비교·분포·지표·도표 요청 | 공식 API/표/다운로드, `raw/`, `processed/`, 증거계획; `statistical_analysis_protocol.md`, `international_statistics_toolkit.md`, `reference_schemas.md` | Statistical Evidence Plan, 원자료·처리자료, 메타데이터, 결과 요약, Chart Plan, 도표와 해석 초안 | 원자료 보존, 파생자료·코드·도표·메타데이터 생성 가능. 수동 복사만으로 재현 불가한 값, 혼합 단위 도표, 값만 나열한 차트 금지 | 값·연도·단위·범위·출처·지표 ID, 변환과 한계 기록; 도표가 절 질문에 답하는지 확인 → S04/S08/S12 |
| S07 절 재서술 | 특정 `section_id`의 보강·교정·확장 | 해당 Markdown, 근거계획·등록자료, 기존 국가특수 내용; `section_rewrite_protocol.md`, 필요 시 S02/S03/S05/S06 참조 | 수정된 정본 Markdown, Section Rewrite Report, 남은 근거 공백 | 요청 절의 Markdown 수정 가능. 국가특수 법·기관·개혁·수치 삭제, 근거 없는 확장, HTML만 수정 금지 | 중심 주장·근거·메커니즘·한계가 적절히 결합되었는지; 인용·수치 재점검 → S09/S12 |
| S08 통계적 서사 통합 | 통계·도표를 원고에 넣거나 통계 주장을 해석 | 검증된 처리자료·도표·메타데이터·대상 절; `statistical_analysis_protocol.md`, `narrative_style_protocol.md` | 수치가 해석된 Markdown 문단, 그림/표 주석, 한계 문장 | 정본 Markdown과 관련 그림 주석 수정 가능. 최신값 하나로 추세·격차·인과를 주장하거나 단위 없는 수치를 삽입하는 일 금지 | 값-메타데이터-도표-본문 추적, 최소 관련 분석 차원(수준·추세·비교·분포) 또는 예외 사유 확인 → S09/S12 |
| S09 장 응집성·서사 문체 | 여러 절/장 개선, 기계적 문체·반복·전환 문제 | 대상 장 전체, 이웃 절, 근거계획; `chapter_coherence_protocol.md`, `narrative_style_protocol.md`, `section_rewrite_protocol.md` | 장 질문, 절 역할표, 전환·중복·불일치 검토, 수정 원고 또는 Narrative Style Review Table | 요청 장의 Markdown 수정 가능. 모든 절에 같은 체크리스트 제목·문단 순서를 강제하거나 감사 언어를 독자용 본문에 넣는 일 금지 | 장 질문에 답하는 종합, 절별 역할·서사 패턴의 구별, 인용 밀도와 문장 리듬 수동 검토 → S12 |
| S10 법·정치 분석 | 헌법, 권력구조, 선거, 법원, 연방·지방 관계, 책임성 | 대상 장 3/4/6 및 원천 법·공식 문서·진단자료; `legal_political_chapter_protocol.md`, S03/S05 | 법적 지위·이행 증거·정치 지표의 분리된 분석, 필요 시 수정 원고 | 요청 절 Markdown·등록자료 수정 가능. 법률=실제 이행, 지수=행정 현실, 제안=제정법으로 동일시하는 일 금지 | 법적 근거·실제 수행·지표 정의·인과 범위의 구분과 절 번호 보존 → S07/S09/S12 |
| S11 행정체계 분석 | 정부조직, 조정, 공무원, 재정관리, 지방집행, 디지털 정부 | 대상 장 5/6/7/16, 기관문서·예산·인사·집행 근거; `administrative_chapter_protocol.md`, S03/S06 | 권한·재정·인사·정보·집행·교정 회로 지도, 관찰 가능한 개혁 함의, 필요 시 수정 원고 | Markdown·편집가능 표·코드 기반 도식 수정 가능. 조직도·회의·대시보드·점수만으로 성과 추론, 증거 없는 인과 주장 금지 | 설계/활동/산출/결과 구분, 자율성과 통제의 긴장, 지표 한계 확인 → S07/S09/S12 |
| S12 품질 게이트·통합 감사 | “출판 준비?”, 광범위 감사, 우선순위 결정 | 전체 국가 패키지, 모든 레지스터, 감사 결과, 렌더 HTML; `quality_gate.md`, `output_templates.md`, S02/S03/S05/S06/S09 | Quality Gate Summary, blocker/warning/수동검토 목록, 준비도와 수정 순서 | 감사 결과·계획 파일 갱신 가능. 자동 감사 통과만으로 준비도를 상향하거나 미해결 위험을 숨기는 일 금지 | `audit_report.py`와 관련 집중 감사 결과를 수동 검토; 3·5·7·16·17과 시각·인용·서사 점검 → S13 또는 보완 모듈 |
| S13 빌드·생성물 보존 | Markdown·빌더 변경 후 HTML 갱신, 링크/자산/렌더 확인 | 정본 원고, 기존 빌더·테스트, 기존 `report/`; `report_structure.md`, `citation_reference_integrity.md` | 재생성 `report/`, 빌드 로그 요약, 보존 비교, 확인 결과 | 기존 빌더를 실행해 생성물 갱신 가능. 빌더 결함을 숨기기 위한 HTML 단독 패치, 관련 없는 생성물 삭제·교체 금지 | 대표 장·절·References 경로, 인용 앵커·외부 링크, 차트·스크립트·내비게이션 보존 확인 → S12 |
| S14 ChatGPT 초안 통합 | 외부 ChatGPT 초안 수신 또는 Evidence Brief 작성 | 대상 절, 검증된 등록자료·통계·공백; `chatgpt_draft_integration.md`, `output_templates.md` | ChatGPT Evidence Brief, Draft Intake Audit, 검증 후 수정된 Markdown 또는 보류 목록 | 정본 수정은 주장·인용·수치의 출처추적 후에만 가능. ChatGPT 출력 자체를 출처로 취급하거나 미검증 풍부화 내용을 유지하는 일 금지 | 새 주장·수치·인용을 하나씩 검증/삭제, 원문 핵심 근거 보존 → S03/S05/S07/S09/S12 |
| S15 학생 실습·프롬프트 지원 | 수업 과제, 학생 피드백, 연구자·학습자용 프롬프트 | 과제 범위, 대상 국가/절 또는 연습 자료; `student_practice_mode.md`, `prompt_templates.md`, `output_templates.md` | 중심 논제, Claim-Evidence-Source Table, 개선 프롬프트, 상위 3개 수정 우선순위, Student Feedback Template | 교수용·연습용 자료 작성 가능. 학생용 결과를 검증된 출판 원고로 표시하거나 미검증 예시를 사실로 제시하는 일 금지 | 산출물이 과제의 국가·절·증거·한계를 명시하는지 확인 → 해당 S01–S14 또는 종료 |

## 3. 모듈 연결 규칙

1. **수정 전 선행 조건**: S07–S11은 최소한 S01의 범위 확인을 거친다. 근거가 약하면 S03/S04를 먼저 수행한다.
2. **수치 선행 조건**: 본문 수치를 새로 넣는 S07/S08/S10/S11은 S06의 메타데이터 또는 동등한 검증 기록을 요구한다.
3. **외부 초안 선행 조건**: S14 출력은 반드시 S03·S05 검증을 지나야 S07로 전달된다.
4. **출판 선행 조건**: S12의 `publication candidate` 판정에는 S05의 인용·링크 검토, S06/S08의 통계·시각 근거, S09의 장 응집성 검토, S13의 재빌드·보존 확인이 필요하다.
5. **충돌 해결**: 모듈 출력이 충돌하면 (a) 원자료·공식법·정본 원고, (b) 검증된 등록자료, (c) 국제 비교지표, (d) 미검증 초안 순으로 우선한다. 해결되지 않으면 사실을 선택하지 말고 `needs_verification`과 인계 질문을 남긴다.

## 4. 최소 인계 예시

```yaml
status: partially_verified
country_code: KHM
scope_checked:
  - 07-02-public-finance.md
outputs:
  - sources/section_evidence_plan.csv: fiscal-risk rows updated
  - processed/statistical_metadata.csv: indicator metadata recorded
files_changed: []
verification:
  - official-source role distinguished from international estimate
  - unit and latest_non_missing_year recorded
open_risks:
  - latest national budget outturn still needs verification
handoff_to: S06 -> S08 -> S07
```

이 봉투는 모듈이 실제 파일을 수정하지 않은 경우에도 사용한다. 따라서 다음 모듈은 “무엇을 했는가”뿐 아니라 “무엇이 아직 확인되지 않았는가”를 기계적으로 추적할 수 있다.
