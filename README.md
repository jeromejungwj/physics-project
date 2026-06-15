# physics-project

수행평가

## Intermediate Axis Theorem 시뮬레이션

비대칭 강체를 중간축으로 돌리면 불안정하게 뒤집히는 **중간축 정리(테니스 라켓
효과 / Dzhanibekov 효과)** 시뮬레이션입니다. Bubbar & Zhu (2025) 논문의 원리와
주요 결과를 재현합니다.

- **Python** (`simulation/`): 토크 없는 오일러 회전방정식을 RK4로 적분 →
  ω-t 그래프, 세 축 안정/불안정 비교, 구-타원체 상태공간(polhode), 세차 주기
  반비례 모델, 3D 뒤집힘 애니메이션. 실행법은 [`simulation/README.md`](simulation/README.md).
- **웹 인터랙티브** (`web/index.html`): 브라우저에서 바로 여는 Three.js 시뮬레이션.
  I₁·I₂·I₃와 초기조건 슬라이더, 실시간 3D 본체, 구-타원체 상태공간, ω(t) 그래프.

```bash
cd simulation && pip install -r requirements.txt && python run_all.py
```
