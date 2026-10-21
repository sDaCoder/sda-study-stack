# Linear Power Supply: Protection Circuits (W1_L1.4)
Source: https://www.youtube.com/watch?v=9ZB3mkm9LeE · IIT Madras – BS in Electronic Systems · 28.0 min

Continues W1_L1.3 (full bridge + linear regulator). The video opens with the regulator already drawn on the board; this lecture adds the protection around it.

## Learning objectives
1. Explain why a linear regulator needs overload protection, and what happens to the series-pass transistor Q1 when R₀ → 0.
2. Explain how a sense resistor R_S and transistor Q2 make a simple current limit, and size it with I_OC · R_S = V_BE ≈ 0.6 V.
3. Derive the foldback equation I₀ = I_SC + (1 − α)V₀ / (αR_S) with α = R_B/(R_A + R_B), and sketch the folding-back V–I curve.
4. Explain the first-cycle (non-repetitive) surge current I_SM in a bridge + capacitor front end, and why switch-on near the peak is the worst case.
5. Explain how transformer leakage inductance and an NTC thermistor limit that surge, and why the NTC's falling resistance matters in steady state.

## Concept flow
The regulator from last lecture works → but a short (R₀ → 0) can destroy Q1 → sense the current with R_S and let Q2 steal Q1's base drive (simple limit, current clamped at I_OC) → better: add a divider so the limit falls as V₀ falls (foldback; short-circuit current I_SC is below rated) → now protect the input side: at switch-on an empty capacitor is a short, giving a huge first-cycle surge → the transformer's leakage inductance helps, and an NTC thermistor adds high resistance when cold and gets out of the way when hot.

## Concepts

### 1. The regulator we're protecting  [00:12]
- **Core idea:** Series-pass BJT Q1 between the unregulated V_i and the load R₀. Divider feeds back aV₀; high-gain error amplifier compares it with V_ref. V_ref comes from a zener regulator with a pot across the zener; moving the pot's tap sets V_ref, so V₀ = V_ref / a.
- **Lecturer's example:** "By adjusting the tap of the pot I can get any value of V reference here to match aV₀."
- **Interactive visual:** Circuit diagram: V_i → Q1 → V₀ → R₀, zener + pot, op-amp, divider. Pot-tap slider (0–100%) moves the wiper on the drawn pot; V_ref and V₀ labels update (V_Z = 6.2 V, a = 0.5, so V₀ = 2·V_ref, capped at V_i − 2 V with V_i = 15 V). Hover/tap blocks to name them.
- **Slide text:** "Pot tap sets V_ref → V₀ = V_ref / a. Now: what if the load shorts?"

### 2. Why overload protection?  [00:54]
- **Core idea:** If R₀ is made very small, I₀ = V₀/R₀ becomes very large. Q1 carries all of it with V_CE ≈ V_i − V₀, so its dissipation P = V_CE · I₀ explodes and "the series pass element will blow off."
- **Interactive visual:** Circuit diagram with R₀ slider (50 Ω → 0.1 Ω, log). Animated current dots along the load path, speed ∝ I₀. Q1 heats up from blue to red, with a "P_Q1" meter (rating 15 W marked). No protection: I₀ unbounded (clipped by a "💥 Q1 destroyed" state above the rating). Values: V_i = 15 V, V₀ = 5 V.
- **Slide text:** "Short the output → I₀ → huge → Q1 dissipates V_CE·I₀ → Q1 fails."

### 3. Simple current limiting with R_S and Q2  [02:11]
- **Core idea:** Put sense resistor R_S in series with Q1's emitter. Q2's base–emitter sits across R_S: V_BE2 = (V₀ + I₀R_S) − V₀ = I₀R_S. Choose R_S so that at the overload current I_OC, I_OC · R_S = 0.6 V. Below I_OC, Q2 is off. At I_OC, Q2 cuts in and its collector diverts current away from Q1's base, pushing Q1 toward cutoff, so the output current stays clamped at I_OC however hard you pull.
- **Lecturer's example:** Node voltages V₀ and V₀ + I₀R_S; "I_OC into R_S as 0.6 V, which is the V_BE drop."
- **Common confusion:** Q2 doesn't switch Q1 off completely; it holds Q1 just at the current where I₀R_S ≈ 0.6 V.
- **Interactive visual:** Circuit diagram with Q1, R_S, Q2 and load. Sliders: R₀ (load) and R_S (0.3–1.2 Ω). Live labels: I₀, V_BE2 = I₀R_S (bar filling to 0.6 V), Q2 state OFF / ON. When Q2 turns on, a second animated current path appears: base drive diverted through Q2 to the output. Beside it, V₀–I₀ plot with the brick-wall limit at I_OC = 0.6/R_S and the live operating point. Q1 power readout. Defaults: V_i = 15 V, V₀ = 5 V, R_S = 0.5 Ω → I_OC = 1.2 A; short → P_Q1 ≈ (15 − 0.6) × 1.2 ≈ 17 W.
- **Slide text:** "V_BE2 = I₀R_S. Set I_OC·R_S = 0.6 V → current clamps at I_OC."

### 4. Foldback current limiting: the circuit  [05:11]
- **Core idea:** The simple limit still delivers I_OC into a short, with nearly all of V_i across Q1. Foldback makes the short-circuit current *smaller than the rated current*. One change: Q2's base is fed from a divider R_A/R_B across the node V₀ + I₀R_S, instead of straight from that node. Q2's emitter stays at V₀.
- **Lecturer's example:** "This is the only change that I'm going to do."
- **Interactive visual:** Circuit diagram with a Simple / Foldback toggle (divider slides in). Same R₀ slider. Labels show node voltages V₀ + I₀R_S, the tap α(V₀ + I₀R_S) and V_BE2 live. Short the load and compare Q1 dissipation: simple ≈ 17 W vs foldback ≈ 5.7 W.
- **Slide text:** "Feed Q2's base through a divider → the limit depends on V₀."

### 5. Deriving the foldback equation  [07:31]
- **Core idea:** With α = R_B/(R_A + R_B) (0 < α < 1):
  V_BE2 = α(V₀ + I₀R_S) − V₀ = αI₀R_S − (1 − α)V₀
  ⇒ I₀ = V_BE2/(αR_S) + (1 − α)V₀/(αR_S).
  Short the output (R₀ = 0 ⇒ V₀ = 0): I_SC = V_BE2/(αR_S). So **I₀ = I_SC + (1 − α)V₀/(αR_S)**.
- **Interactive visual:** Step-through derivation (Next/Prev, 5 steps). Each step highlights the matching node/part on a mini circuit (e.g. step 1 highlights the divider tap; step 4 sets V₀ = 0 and greys the term out).
- **Slide text:** "I₀ = I_SC + (1 − α)V₀/(αR_S). At V₀ = 0 only I_SC is left."

### 6. The foldback V–I curve  [10:29]
- **Core idea:** Plot V₀ (y) vs I₀ (x). Normal operation: V₀ is flat up to the knee, I_knee = I_SC + (1 − α)V₀/(αR_S). Pull harder and the operating point slides down a straight line back to I_SC at V₀ = 0. Since the second term is positive, I_SC < I_knee: the current "folds back."
- **Interactive visual:** V–I plot with sliders α (0.5–0.95) and R_S (1–3 Ω), plus R₀ slider moving the operating point (intersection of the load line V = I·R₀ with the curve). Simple-limit curve drawn dashed for comparison. Readouts: I_knee, I_SC, P_Q1 at the operating point. Defaults: α = 0.75, R_S = 2 Ω, V₀ = 5 V, V_BE = 0.6 V → I_SC = 0.4 A, I_knee ≈ 1.23 A.
- **Going further:** Foldback can latch up with constant-current loads at start-up (Wikipedia: Current limiting).
- **Slide text:** "Foldback: rated current up to the knee, then I falls to I_SC < I_rated."

### 7. The first-cycle surge current  [12:04]
- **Core idea:** At switch-on the filter capacitor is empty. A step of voltage gives huge dV/dt, the capacitor looks like a short, and only the diode and winding resistances limit the current. The first cycle has to put in the whole ½CV₁²; later cycles only top up what the load drew. Switch-on happens at a random point of the sine; the worst case is near the peak V₁. The same charge must then go in during a much narrower window, so the peak current is far higher: I ≈ V₁ / (2r_D + R_w). This is the non-repetitive surge current I_SM; ignore it and the diodes or capacitor blow in the first half-cycle.
- **Interactive visual:** Circuit diagram (source + switch → bridge → C ∥ R₀) above a scope with |v_G|, v_C and i_D over 3 cycles. Slider: switch-on angle 0–180°; button "Switch on". Readouts: first-cycle peak i_D vs steady-state peak, ratio. Model: V₁ = 20 V peak, 50 Hz, r_D = 0.1 Ω × 2, R_w = 0.3 Ω, C = 4700 µF, R₀ = 18 Ω (≈1 A). At 90° the first peak is ≈ 40 A vs a few amps in steady state.
- **Slide text:** "Empty C = short. Switch on near the peak → I_SM ≈ V₁ / (2r_D + R_w)."

### 8. Leakage inductance helps  [20:39]
- **Core idea:** A practical transformer is a T network: primary leakage L_σP, secondary leakage L_σS in series, magnetising M and core-loss R_C in shunt (large, ignore for the surge). The surge path runs through L_σP + L_σS → diode → C → diode, so the leakage inductance limits the surge. That's why many transformer-fed supplies need no extra protection; the lecturer still recommends adding some.
- **Interactive visual:** T-equivalent circuit diagram with the surge path animated (arrows through L_σP, L_σS, bridge, C). Slider: total leakage L_σ (0–3 mH). Same scope as concept 7 at a 90° switch-on, showing the peak drop and the softer rise. Readouts: X_L = ωL_σ, I_SM.
- **Slide text:** "Leakage inductance L_σP + L_σS sits in the surge path and limits it."

### 9. NTC thermistor inrush limiter  [22:57]
- **Core idea:** Put an NTC (negative temperature coefficient) thermistor in series. Cold, its resistance is high, so it limits the first-cycle surge: I ≈ V / |jω(L_σP + L_σS) + R_NTC|. Current heats it (I_rms²R), its resistance drops, and in steady state it wastes little power. The lecturer's sketch: 10 Ω cold → about 5 Ω hot.
- **Lecturer's example (datasheet):** inrush-limiting NTC: R at 25 °C = 22 Ω ±20 %, max steady-state current 1 A, R at max current ≈ 0.95 Ω (the caption says "95 ohms"; 0.95 Ω is consistent with the other datasheet numbers), thermal time constant 30 s, dissipation coefficient 11 mW/°C. Power-vs-temperature derating falls linearly to near zero by ~100 °C.
- **Interactive visual:** Circuit diagram with the thermistor in the mains line (direct-to-mains case, V₁ = 325 V), its body colour shifting with temperature. Time scrubber 0–150 s after switch-on and a steady-state I_rms slider (0.2–1 A). Plots: R_NTC(t) and P_loss(t). Readouts: inrush peak at t = 0 (325 V / 22 Ω ≈ 15 A vs ≈ 650 A with only ~0.5 Ω), steady R and loss vs a fixed 22 Ω resistor (22 W at 1 A vs ≈ 0.9 W). Thermal model: dissipation δ = 11 mW/°C, τ = 30 s, R(T) = 22·exp(B(1/T − 1/298 K)) with B ≈ 4000 K (assumed; reproduces 0.95 Ω at 1 A).
- **Slide text:** "Cold NTC: high R stops the surge. Hot NTC: low R, low loss."

## Check your understanding
1. **In the simple limit, R_S = 0.3 Ω. Roughly what is I_OC?** A) 0.3 A B) 2 A C) 6 A. **B.** I_OC = 0.6 V / 0.3 Ω = 2 A.
2. **The output is shorted. Which delivers less current?** A) Simple limit B) Foldback C) Same. **B.** Foldback gives I_SC = V_BE/(αR_S), below the rated current; the simple limit still delivers I_OC.
3. **With foldback, what sets the knee current above I_SC?** A) (1 − α)V₀/(αR_S) B) V_BE/R_S C) V_i/R₀. **A.** That term vanishes when V₀ = 0.
4. **When is the first-cycle surge worst?** A) Switch-on at the zero crossing B) Switch-on near the peak C) Always the same. **B.** The empty C sees almost V₁ at once and has the shortest window to charge.
5. **Why an NTC rather than a fixed resistor?** A) It's cheaper B) High R cold limits the surge, low R hot cuts steady-state loss C) It filters ripple. **B.**
6. **Why do transformer-fed supplies often get away without surge protection?** **Leakage inductance (L_σP + L_σS) in the surge path limits the current.**

## Recap
- Q1 must be protected: a short makes I₀ huge and P_Q1 = V_CE·I₀ destroys it.
- Simple limit: V_BE2 = I₀R_S, so current clamps at I_OC = 0.6 V / R_S.
- Foldback: a divider on Q2's base gives I₀ = I_SC + (1 − α)V₀/(αR_S); into a short the current drops to I_SC.
- At switch-on an empty capacitor draws a non-repetitive surge I_SM, worst near the AC peak.
- Leakage inductance and a cold NTC thermistor limit the surge; the NTC's resistance falls as it heats, so steady-state loss is small.

## Sources
- Video: "W1_L1.4: Linear power supply", IIT Madras BS in Electronic Systems: https://www.youtube.com/watch?v=9ZB3mkm9LeE (backbone of all content and derivations).
- Wikipedia, "Current limiting": https://en.wikipedia.org/wiki/Current_limiting (confirms the 0.65/R_sense limit, foldback's purpose and the lock-up caveat, and NTC inrush limiting).
- Texas Instruments, LDO foldback current limit note (SBVA097): https://ti.com/document-viewer/lit/html/SBVA097/GUID-BB1741F4-005F-4D8F-A92C-DE8F32051042 (real-world foldback numbers: I_CL 720 mA folding back to I_SC 350 mA; start-up caveat).
- Previous lecture brief, `lectures/full-bridge-linear-regulator/lecture-brief.md` (regulator and zener reference this lecture builds on).
