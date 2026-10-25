"""UI / prompt language. PMPREDICT_LANG=ko (default) or en; the agent answers in that language and the web UI uses its labels."""
from __future__ import annotations

import os


def lang() -> str:
    return "en" if os.environ.get("PMPREDICT_LANG", "ko").lower().startswith("en") else "ko"


_T = {
    "ko": {
        "loading": "모델·데이터 로딩...", "no_file": "(파일 없음)", "rows_shown": "{n}행 중 200행 표시", "show_fail": "표시 실패",
        "error": "오류", "tool_json": "도구 결과 JSON", "no_result": "(결과 없음)", "backend": "LLM 백엔드", "model": "모델",
        "default": "(기본)", "backend_status": "백엔드 상태",
        "keys_caption": "키: anthropic {a} · openai {o} (값은 표시하지 않음). 구독 경로(Claude/Codex)는 이 PC의 개인 사용 전용이며 웹 배포에 쓰지 않습니다.",
        "new_session": "(새 세션)", "session": "세션", "start_new": "새 세션 시작", "examples": "**예시 질문**",
        "legacy": "직접 실행 (기존 폼)",
        "intro": "배합 → 성능 예측 · 목표 → 배합 역설계 · 노즐/구조물 → 빌더빌리티와 프린팅 스케줄 · 문헌 검색 · 문헌 DB 질의. "
                 "수치는 모두 도구 결과이며 80 % 구간과 함께 제시됩니다. 유변 예측은 자릿수 참고용입니다.",
        "chat_placeholder": "무엇을 도와드릴까요? (예: 'w/b 0.35 3DCP 모르타르 정적항복응력 예측')",
        "init_fail": "백엔드 초기화 실패", "running": "실행 중…", "last_turn": "마지막 턴: in {i} / out {o} 토큰", "cache": "캐시",
        "page": "페이지", "err_prefix": "[오류]", "recent": "최근 대화 (자동 요약 불가, 마지막 6턴):",
        "labels": {"anthropic": "Anthropic API", "openai": "OpenAI API", "claude_sdk": "Claude 구독 (Agent SDK)",
                   "codex": "ChatGPT 구독 (Codex CLI)", "fake": "테스트용 가짜 프로바이더"},
        "examples_list": [
            "OPC 모르타르 w/b 0.40, s/b 2.0, PCE 0.5 %의 28일 압축강도와 플로우를 예측해줘",
            "25 mm 노즐로 높이 600 mm, 길이 1.5 m 벽(2필라멘트)을 50 mm/s로 뽑으려고 해. 정적항복 3 kPa, Athix 1 Pa/s인 재료면 되는지 판정하고 사이클 시간 창을 알려줘",
            "3DCP 논문 중 VMA를 쓴 논문이 몇 편이고, 그 믹스들의 정적항복응력 중앙값은?",
            "28일 압축 ≥ 40 MPa, 정적항복 1–4 kPa인 문헌 배합 10개를 찾아줘 (3DCP 우선)",
            "위 조건으로 클링커 최소화 배합을 역설계해줘 (OPC 필수, 실리카퓸·석회석 허용)",
        ],
    },
    "en": {
        "loading": "Loading models and data...", "no_file": "(file missing)", "rows_shown": "showing 200 of {n} rows", "show_fail": "cannot display",
        "error": "error", "tool_json": "Tool result JSON", "no_result": "(no result)", "backend": "LLM backend", "model": "Model",
        "default": "(default)", "backend_status": "Backend status",
        "keys_caption": "keys: anthropic {a} · openai {o} (values are never shown). Subscription backends (Claude/Codex) are for personal use on this PC only; do not deploy them on a public server.",
        "new_session": "(new session)", "session": "Session", "start_new": "Start new session", "examples": "**Example questions**",
        "legacy": "Direct mode (legacy forms, Korean)",
        "intro": "Mix → property prediction · targets → inverse mix design · nozzle/structure → buildability and print schedule · literature search · literature DB queries. "
                 "Every number comes from a tool result and is shown with its 80 % interval. Rheology predictions are order-of-magnitude guidance.",
        "chat_placeholder": "How can I help? (e.g. 'predict the static yield stress of a w/b 0.35 3DCP mortar')",
        "init_fail": "backend initialisation failed", "running": "running…", "last_turn": "last turn: in {i} / out {o} tokens", "cache": "cache",
        "page": "Page", "err_prefix": "[error]", "recent": "Recent conversation (automatic summary unavailable, last 6 turns):",
        "labels": {"anthropic": "Anthropic API", "openai": "OpenAI API", "claude_sdk": "Claude subscription (Agent SDK)",
                   "codex": "ChatGPT subscription (Codex CLI)", "fake": "fake provider (tests)"},
        "examples_list": [
            "Predict the 28-day compressive strength and flow of an OPC mortar with w/b 0.40, s/b 2.0 and 0.5 % PCE",
            "I want to print a 600 mm high, 1.5 m long wall (2 filaments) with a 25 mm nozzle at 50 mm/s. Is a material with static yield stress 3 kPa and Athix 1 Pa/s printable? Give the cycle-time window.",
            "How many 3DCP papers use a VMA, and what is the median static yield stress of their mixes?",
            "Find 10 published mixes with 28-day compressive strength >= 40 MPa and static yield stress 1-4 kPa (prefer 3DCP)",
            "Inverse-design a minimum-clinker mix for those targets (OPC required, silica fume and limestone allowed)",
        ],
    },
}


def T(key: str, **kw) -> str:
    v = _T[lang()][key]
    return v.format(**kw) if kw and isinstance(v, str) else v


def labels() -> dict:
    return _T[lang()]["labels"]


def examples() -> list[str]:
    return _T[lang()]["examples_list"]


ROLE_EN = """You are the pmpredict agent: the cement paste / mortar mix-design assistant of the 3D concrete printing (3DCP) laboratory at Sungkyunkwan University.
Your tools are prediction models trained on a literature database (mix designs, properties, rheology and printing results extracted from thousands of papers), an inverse-design engine, a buildability calculator, literature retrieval and read-only SQL.
Answer in English, concisely. Tool descriptions and some tool messages are in Korean: translate anything you quote from them. No emoji."""

GUARDRAILS_EN = """Rules
1. Never invent numbers. Every quantitative statement must come from a tool result in this conversation; predictions are written as q50 [q10, q90] with units.
2. For targets flagged weak_model (most rheology and flow targets) say that the value is order-of-magnitude guidance and present published analogue mixes (retrieve_literature, candidate analogues) as the primary evidence. If n_range_violations > 0 say the prediction extrapolates beyond the training range.
3. Build mixes with the class names and conventions from describe_vocabulary, and state explicitly which defaults you used for values the user did not give (age 28 d, comp_cube50, moist curing, s/b, ...).
4. For database questions call describe_schema first, then sql_query. All master.db columns are TEXT (CAST is needed) and empty strings are missing values. Distinguish paper counts from mix counts.
5. Slow tools (design_mix, design_for_print_job; 30–150 s): run them immediately when the user has given targets and a search space; otherwise confirm targets and space in one sentence, once, then run.
6. Buildability: the physical verdict (Roussel plastic collapse + structuration, Suiker free-wall buckling, open time) is primary; the empirical collapse probability is secondary. When the verdict is non_printable, give actionable alternatives (cycle-time window, layer height, required tau_s(0)/Athix, accelerator, VMA, lower w/b).
7. Report the paths of files the tools created (figures, CSV, reports). Use save_report when the user wants a summary saved; use remember when the user says "remember".
8. On a tool error explain the cause in one line, fix the input and retry (at most twice). Say so when you do not know.
9. The models are correlations in published data and do not replace experiments; add briefly, when relevant, that the final mix needs experimental verification."""
