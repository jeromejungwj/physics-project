# Intermediate Axis Theorem — Simulation

A numerical simulation of the **intermediate axis theorem** (a.k.a. the
*tennis-racquet effect* or *Dzhanibekov effect*), reproducing the physics and
key results of:

> Bubbar, F. & Zhu, L. (2025). *The Intermediate Axis Theorem: A Model for the
> Period and a Phenomenal Explanation.* Science One Programme, UBC.
> (Paper materials: https://github.com/fbubbar/sci1-t2)

When a rigid body with three distinct principal moments of inertia
(I₁ > I₂ > I₃) is spun about its **intermediate** axis, the motion is unstable
and the body periodically flips. Spinning about the largest or smallest axis is
stable. The simulation integrates the **torque-free Euler rotation equations**

```
I₁ ω̇₁ = (I₂ − I₃) ω₂ ω₃
I₂ ω̇₂ = (I₃ − I₁) ω₃ ω₁
I₃ ω̇₃ = (I₁ − I₂) ω₁ ω₂
```

with a 4th-order Runge–Kutta scheme, alongside an orientation quaternion so the
body can be drawn in 3D. Energy and |L| are conserved to ~machine precision,
which validates the integrator.

## What's here

| File | What it produces |
|------|------------------|
| `physics.py` | Core RK4 integrator (ω + orientation quaternion), conserved quantities. Run it for a conservation self-test. |
| `fig_omega_graphs.py` | ω(t) time series of the flip (paper Fig. 5 style) + a 3-panel **stable/unstable comparison** of the three axes (added for teaching; not a specific paper figure). |
| `fig_polhode.py` | The **sphere ∩ ellipsoid** state-space construction and the polhode curves (paper Figs. 1–3). |
| `fig_period_model.py` | **Precession period vs. initial speed**, fitting the inverse model `T = a/(ω₀+b)+c` to simulated data (paper Fig. 12; the paper's own racquet fit was a=11.85, b=2.30, c=0.047, χ²=1.58). |
| `animate_racquet.py` | A 3D GIF of the racquet **flipping** about the intermediate axis, with the conserved L vector. |
| `run_all.py` | Generates every figure and the animation. |

The companion **interactive web version** lives in `../web/index.html`
(open it in any browser — sliders for I₁, I₂, I₃ and the initial conditions,
live 3D body, the sphere/ellipsoid state space, and a scrolling ω(t) plot).

## Run it

```bash
cd simulation
pip install -r requirements.txt
python run_all.py          # everything -> figures/
# or individually:
python physics.py          # integrator conservation self-test
python fig_omega_graphs.py
python fig_polhode.py
python fig_period_model.py
python animate_racquet.py
```

Outputs are written to `simulation/figures/`.

## Reproduced results

- **Unstable flip about r₂ only.** ω₂ periodically reverses sign while ω₁ and ω₃
  spike during each flip; rotation about r₁ and r₃ stays steady.
- **State-space geometry.** The motion follows the intersection of the |L|
  sphere and the energy ellipsoid; about the intermediate axis this curve wraps
  the whole sphere (the source of the instability).
- **Period ∝ 1/ω₀.** The flip period follows the inverse relation the paper
  fitted to racquet data, here recovered directly from the simulation.

---

## 한국어 설명 — 어떤 값을 쓰는가

**이론(물리 법칙)은 웹과 파이썬이 동일합니다.** 두 버전 모두 토크 없는
오일러 회전방정식을 같은 방식으로 풀며, 바뀌는 것은 "어떤 물체(관성모멘트)를
어떤 초기조건으로 돌리느냐"뿐입니다. 관성모멘트는 물체마다 다르므로 정해진
"이론값"은 없고, 이론에 해당하는 것은 **오일러 방정식 그 자체**입니다.

### 웹 (`../web/index.html`) — 실시간 조절 가능
- I₁·I₂·I₃, 초기 각속도(spin), 섭동(eps) 슬라이더를 움직이면 **그 자리에서
  다시 계산**됩니다(미리 만든 영상이 아니라 매 프레임 RK4 적분).
- 프리셋: `textbook` = (3, 2, 1), `racquet` = (3, 2.9, 0.6).
  라켓 프리셋은 "I₁≈I₂, I₃는 작다"는 **비율만 흉내**낸 것이며, 논문의 실제
  측정값(아래)이 아닙니다(임의 단위).
- 즉 원하는 값으로 자유롭게 바꿔가며 실험할 수 있습니다.

### 파이썬 (이 폴더) — 고정값으로 그림 생성
- 모든 그림 스크립트는 **`TEXTBOOK_INERTIA = (3, 2, 1)`** 와 각 스크립트에
  하드코딩된 초기조건을 사용합니다(보고서용 정지 그림을 깔끔하게 뽑기 위함).
- 논문 실측값 **`RACQUET_INERTIA = (78, 78, 1.391) g·m²`** (Table 2)은
  `physics.py`에 **참조용 상수로만** 들어 있고 그림 생성에는 쓰이지 않습니다.
  논문에서는 I₁과 I₂가 거의 같아(측정 오차 범위 내) 뒤집힘이 매우 느리므로,
  시각적으로 분명한 그림을 위해 잘 분리된 교과서 값을 사용했습니다.
- 다른 값으로 그림을 뽑으려면 스크립트의 `I=TEXTBOOK_INERTIA` 인자를 바꾸면
  됩니다.

| | 사용하는 관성모멘트 | 값 조절 | 논문 실측값 사용? |
|---|---|---|---|
| 웹 | 기본 (3,2,1) / 라켓 (3,2.9,0.6) | 슬라이더로 실시간 | ✗ (비율만 흉내) |
| 파이썬 | (3,2,1) 고정 | 코드 수정 필요 | ✗ (참조 상수로만 보관) |

> 참고: 논문의 (78, 78, 1.391)은 "이론값"이 아니라 **진자 실험으로 측정한 값**
> 입니다(Table 2).
