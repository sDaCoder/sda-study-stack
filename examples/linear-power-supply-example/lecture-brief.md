# Example: Linear Power Supply (W1_L1.6)
Source: https://www.youtube.com/watch?v=uUPryFq32oY · IIT Madras – BS in Electronic Systems · 24.0 min

A design exercise that ties together everything from Week 1 (full bridge + capacitor filter, discrete linear regulator, reference, foldback limit, NTC surge limiting) and introduces IC regulators (LM317, LM723, 78xx). The user asked for **interactive circuit diagrams** on every concept slide: each widget below is built around a drawn schematic that reacts to the controls.

## Learning objectives
1. Lay out a three-output bench supply (two 15 V, one 5 V) from a 230 V multi-winding transformer, and say which regulator suits each output.
2. Work out the unregulated voltage window for ±20 % mains, and from it the V_CE range and worst-case dissipation of the series-pass transistor Q1, then size a heat sink.
3. Explain what R5 and the zener-fed op-amp supply protect, and choose their values from worst-case conditions.
4. Set an LM317's output with V₀ = 1.25 V (1 + R2/R1), and keep any IC regulator above its ≈3 V input–output headroom.
5. Plan the line-regulation and load-regulation experiments and read the resulting V₀–V_i and V₀–I₀ plots.

## Concept flow
The brief (3 outputs from one transformer) → what the lab transformer offers → output 1: the full discrete regulator we have built over the week → its input window under mains tolerance → what that means for Q1's heat → protecting the op-amp (R5) and powering it (zener tap) → output 2: the same job done by an LM317 → the LM723, which is our discrete circuit in one chip → output 3: a 7805 and its headroom rule → finally, test all three with line and load regulation.

## Concepts

### 1. The project: a three-output supply  [00:32]
- **Core idea:** Mains 230 V → switch/MCB → a step-down, 50 Hz, laminated multi-winding transformer with three secondaries. Each secondary gets its own chain: NTC thermistor → full bridge → capacitor → regulator. Outputs: 15 V (discrete regulator), 15 V (LM317), 5 V (7805).
- **Lecturer's example:** "Two 15 volts and one 5 volts… use some IC regulators for the other two windings."
- **Interactive visual:** Full block-level circuit diagram: mains plug, MCB switch, transformer with three secondaries, and three chains (NTC, bridge, C, regulator, load). Click the MCB to switch on (current dots start flowing). Click an output tab (Discrete 15 V / LM317 15 V / 7805 5 V) to highlight that chain and show its summary card (winding used, unregulated range, regulator type, headroom).
- **Slide text:** "One transformer, three windings, three independent regulated rails."

### 2. Inside the lab transformer  [02:14]
- **Core idea:** A laboratory transformer has EI laminations, a varnished wound coil and terminal lugs on top. Primary: 0–230 V (red and black). Three centre-tapped secondaries: 12-0-12, 15-0-15, 9-0-9 V rms. End-to-end gives double (24, 30, 18 V); end-to-centre gives the single value. The centre tap allows a centre-tapped rectifier; otherwise use the two ends or one end plus centre.
- **Interactive visual:** Transformer drawing with the 9 secondary lugs. Click any two lugs on the same winding to "probe" them: a voltmeter reads V_rms, V_peak = √2·V_rms, and the unregulated DC after a bridge ≈ V_peak − 2·V_D (0.7 V). Picking lugs on different windings gives a "not connected (isolated windings)" message.
- **Slide text:** "12-0-12: ends = 24 V, end-to-centre = 12 V."

### 3. Output 1: the discrete regulator, all together  [04:56]
- **Core idea:** Every block from the week in one schematic: series-pass BJT Q1 driven by the op-amp through R5; reference = R3 + zener, with potentiometer R4 tapping V_ref into the op-amp's + input; output sensing divider R1/R2 feeding aV₀ into the − input; current sense R_S with Q2 and divider R_A/R_B forming the foldback limit; load R₀.
- **Lecturer's example:** "Let us mark the components… R1, R2 to get aV₀… R_S current sense… R_A, R_B… R3, R4 for the reference… R5 limits the current so the op-amp doesn't get damaged."
- **Interactive visual:** The full schematic, each component a clickable hotspot. Clicking a part highlights it and its function group (Pass element / Reference / Feedback / Foldback limit / Op-amp protection), with a one-line role and how it's chosen. A "Trace the loop" step-through (4 steps) animates: V_ref → op-amp → R5 → Q1 base → V₀ → R1/R2 → back to the − input.
- **Slide text:** "Pass element · reference · feedback · foldback · op-amp protection."

### 4. The unregulated window and Q1's dissipation  [07:51]
- **Core idea:** 12-0-12 used end-to-end = 24 V rms → peak ≈ 24√2 ≈ 34 V (diode drops ignored, as in the lecture). With mains 230 V ± 20 %, the capacitor voltage moves from ≈27 V to ≈40 V. Output 15 V at 1 A (15 W). V_CE(Q1) = V_C − 15 V and P_Q1 = V_CE · I₀.
- **Lecturer's example:** V_CE "from 12 to 35 volts", P_D from 12 W to 35 W, "for 15 W output you need 50 W" from the bridge/capacitor stage.
- **Common confusion / correction:** The lecturer's high-end subtraction slips: 40 − 15 = **25 V**, not 35 V. So P_Q1 ranges 12 W → 25 W and the front end must supply 15 + 25 = **40 W**. The design lesson is unchanged: size the heat sink for the high-mains corner, not the nominal one. The deck shows the corrected numbers and notes the slip.
- **Interactive visual:** Circuit: mains source (with a ±20 % tolerance slider) → transformer → bridge → C → Q1 → load R₀. Second slider: load current 0–1 A. Live labels on the schematic: V_C, V_CE, V₀ = 15 V, I₀. Q1's body colour heats from cool to red with P_Q1; bar meters for P_out, P_Q1 and P_in, plus efficiency η = 15/V_C. Markers at the −20 % and +20 % corners.
- **Slide text:** "High mains → biggest V_CE → most heat. Design for the worst corner."

### 5. Sizing Q1's heat sink  [09:11]
- **Core idea:** Junction temperature must stay below T_J,max (150 °C for these parts). Heat flows through a "thermal circuit" of series resistances: junction→case θ_JC, case→sink θ_CS, sink→ambient θ_SA. T_J = T_A + P_D(θ_JC + θ_CS + θ_SA), so the sink must satisfy θ_SA ≤ (T_J,max − T_A)/P_D − θ_JC − θ_CS. (TI's LM317 datasheet gives this same equation.)
- **Lecturer's example:** "Choose the heat sink such that 35 W can be dissipated without… the junction temperature crossing T_J max."
- **Interactive visual:** Thermal circuit drawn as a resistor ladder: a current source P_D at the junction node, then θ_JC, θ_CS, θ_SA down to the T_A "ground". Sliders: P_D (5–40 W, default 25 W, with a marker at the lecturer's 35 W), T_A (25–50 °C), and the heat-sink θ_SA (0.5–10 °C/W). Node temperatures update along the ladder; T_J turns red above 150 °C. Readout: the largest θ_SA allowed. Values: θ_JC = 1.5 °C/W (TO-220 power BJT), θ_CS = 0.5 °C/W (with grease).
- **Slide text:** "θ_SA ≤ (T_J,max − T_A)/P_D − θ_JC − θ_CS."

### 6. R5: protecting the op-amp  [10:22]
- **Core idea:** Op-amps can source only 10–50 mA. Don't draw more than 75 % of the rating. The worst case is a shorted output: V₀ = 0, so Q1's base sits at only I₀R_S + V_BE ≈ 1.2 V, Q2 is sinking the drive, and nearly the whole op-amp output voltage appears across R5. So choose R5 ≥ (V_OA − V_B1) / (0.75 · I_rated).
- **Lecturer's example:** "If it's a 50 mA op-amp, draw 35 mA… if it's a 20 mA op-amp, don't draw more than 15 mA."
- **Interactive visual:** Zoomed schematic: op-amp → R5 → Q1 base, Q2 from Q1's base to the output, R_S, load R₀ with a "Short output" toggle. Sliders: R5 (100 Ω–2 kΩ) and op-amp rating (20 / 50 mA buttons). Readout: op-amp current as an animated dot stream plus a bar against the 75 % line; the op-amp turns red when the limit is exceeded. Values: op-amp output ≈ 14 V (15 V rail), V_B1 = 0.6 + 0.6 = 1.2 V at short; normal operation V_B1 = 15 + 0.6 + 0.6 ≈ 16.2 V (op-amp then sits near its rail, little current through R5). Show the R5 the rule gives (≈ 340 Ω for 50 mA: (14 − 1.2) V / 37.5 mA).
- **Slide text:** "Worst case is V₀ = 0. Keep I_R5 ≤ 75 % of the op-amp's rating."

### 7. Powering the op-amp from the unregulated rail  [11:51]
- **Core idea:** The unregulated rail swings 27–40 V, but the op-amp needs a steady 15 V. Tap it with a series resistor + 15 V zener (a shunt regulator). Design the zener for about 25–30 mA.
- **Lecturer's example:** "Tap off a resistor and a zener… design the zener to handle around 25 to 30 milliamps."
- **Interactive visual:** Schematic: V_C (slider 27–40 V) → R_Z → node V_CC = 15 V with zener to ground and the op-amp as a load (slider 0–15 mA). R_Z = 820 Ω (designed so at 27 V and full load the zener still gets ≥ 5 mA). Live: I_R = (V_C − 15)/R_Z, I_Z = I_R − I_opamp, zener power, current arrows sized by value. Warnings: I_Z < 2 mA ("zener drops out of regulation") or P_Z over rating. At 40 V and no load: I_Z ≈ 30 mA, P_Z ≈ 0.46 W.
- **Slide text:** "R + zener turns a 27–40 V swing into a steady 15 V for the op-amp."

### 8. Output 2: LM317 adjustable regulator  [12:51]
- **Core idea:** Three pins: in, out, adjust. The LM317 holds 1.25 V between OUT and ADJ, so I = 1.25/R1 flows through R1. The ADJ pin draws almost nothing (I_ADJ ≈ 50 µA), so the same current flows through R2: V₀ = 1.25 (1 + R2/R1) (+ I_ADJ·R2, usually negligible). It handles ≈1.5 A and has internal short-circuit limiting and thermal shutdown. It needs V_in − V_out > 3 V.
- **Lecturer's example:** Set to 15 V by choosing R1, R2. Datasheet: output 1.25 V upward, > 1.5 A, T_J ≤ 150 °C, θ_JA ≈ 38 °C/W (TO-263).
- **Interactive visual:** LM317 schematic: V_in → LM317 → V₀, R1 from OUT to ADJ, R2 from ADJ to ground, load. Sliders: R1 (100–1000 Ω, default 240 Ω) and R2 (0–5 kΩ, default 2.64 kΩ → 15.0 V). The 1.25 V across R1 is annotated, the current arrow 1.25/R1 runs through both resistors, and V₀ updates (with and without the I_ADJ term). A V_in slider (5–40 V) shows a "dropout!" state when V_in − V₀ < 3 V (output collapses to V_in − 3). Readout: P = (V_in − V₀)·I₀, with I₀ = 1 A.
- **Slide text:** "V₀ = 1.25 V × (1 + R2/R1). Keep V_in ≥ V₀ + 3 V."

### 9. LM723: our discrete circuit inside one chip  [14:50]
- **Core idea:** The LM723's internal schematic contains the same blocks as the discrete regulator: a zener-based voltage reference (V_ref brought out to a pin), an error amplifier, a series-pass transistor, and a current-limit transistor whose base–emitter is brought out to pins CL/CS so you connect your own R_S. For more current, add an external boost transistor as a Darlington with the internal pass transistor.
- **Lecturer's example:** "Almost all the parts of the circuit that we discussed fall into the IC."
- **Interactive visual:** Side-by-side: the discrete schematic (left) and the LM723 functional block diagram (right, with pin names V_REF, NI, INV, V_C, V_OUT, CL, CS). Click a block on either side (Reference, Error amp, Series pass, Current limiter, Sense resistor) to light up its twin on the other side and show "inside the IC" vs "you add externally" (R_S, divider, boost transistor). A "Add boost transistor" toggle draws the external Darlington stage.
- **Slide text:** "Reference + error amp + pass + limiter = LM723. You add R_S and the divider."

### 10. Output 3: the 7805 and the headroom rule  [19:24]
- **Core idea:** 78xx fixed regulators (7805 = 5 V, 7808, 7810, 7812, 7815): three terminals (in, out, common), up to 1.5 A, internal protection, no external parts needed. They need V_in − V₀ > 3 V (the lecture's design rule; TI lists ≈ 2 V typical dropout at 1 A). For the 7805 the capacitor voltage must stay **above 8 V under all conditions**, including the bottom of the ripple at low mains. Heat sinks are needed for the 7805, LM317 and Q1 alike.
- **Lecturer's example:** "This capacitor point voltage should be greater than 8 volts under any condition. So choose the values of the winding accordingly."
- **Interactive visual:** Schematic: winding → bridge → C → 78xx → load, plus a scope below showing the capacitor's ripple waveform (2 cycles at 100 Hz ripple) and the output. Buttons: 7805 / 7812 / 7815. Sliders: winding (6–18 V rms), mains tolerance (−20 to +20 %), load current (0.1–1.5 A); C = 2200 µF fixed. Ripple ΔV ≈ I₀/(2fC). The scope draws the V₀ + 3 V headroom line; wherever V_C dips below it, the output trace sags and the region is shaded red. Readouts: V_C,min, headroom, P_reg = (V_C,avg − V₀)·I₀.
- **Slide text:** "V_C must stay ≥ V₀ + 3 V at the valley of the ripple, at low mains."

### 11. Testing: line and load regulation  [22:06]
- **Core idea:** Two experiments for each supply. **Line regulation:** vary V_i with an autotransformer (variac) on the primary, keep the load fixed, tabulate about 5 readings of V₀ vs V_i and plot (V_i on x, V₀ on y). **Load regulation:** keep V_i fixed, vary R₀ to change I₀, tabulate and plot V₀ vs I₀. A good regulator gives flat lines.
- **Lecturer's example:** "x-axis keep V_i and V₀ on the y-axis… x-axis the independent variable I₀."
- **Interactive visual:** Bench schematic: variac knob → transformer → bridge + C → regulator (switchable: Discrete / LM317 / 7805) → ammeter → R₀ with voltmeters on V_i and V₀. Sliders: variac (160–280 V mains) and R₀. "Record reading" button adds a row to a small table and a point to the matching plot (two tabs: V₀ vs V_i and V₀ vs I₀). Model: in regulation V₀ = V_nom + small line/load error (≈0.1 %); below V₀ + 3 V headroom V₀ follows V_i − 3; the discrete supply folds back past ≈1.2 A, the ICs current-limit at ≈1.5 A. So the learner's plots can show the flat region, the dropout knee and the current limit.
- **Slide text:** "Line: V₀ vs V_i (vary with a variac). Load: V₀ vs I₀ (vary R₀)."

## Check your understanding
1. **A 15-0-15 winding, used end-to-end. Roughly what peak voltage reaches the capacitor (ignore diode drops)?** A) 15 V B) 21 V C) 42 V. **C.** 30 V rms × √2 ≈ 42 V.
2. **Mains is +20 %, the discrete supply gives 15 V at 1 A from V_C = 40 V. What does Q1 dissipate?** A) 15 W B) 25 W C) 40 W. **B.** (40 − 15) V × 1 A = 25 W.
3. **When is the op-amp most at risk of over-current through R5?** A) At no load B) With the output shorted C) At high mains. **B.** V₀ = 0 drops Q1's base to ≈1.2 V, so almost the whole op-amp voltage sits across R5.
4. **LM317 with R1 = 240 Ω. What R2 gives about 5 V?** A) 240 Ω B) 720 Ω C) 2.4 kΩ. **B.** 1.25 (1 + 720/240) = 5 V.
5. **A 7805's capacitor ripples between 7.4 V and 9 V. What happens?** A) Fine, the average is above 8 V B) The output dips at every ripple valley C) The 7805 overheats. **B.** The headroom rule must hold at the valley, not on average.
6. **In a load-regulation test, which is the independent variable?** A) V₀ B) I₀ (set by R₀) C) V_i. **B.** Vary R₀ to set I₀, then plot V₀ against it.

## Recap
- One multi-winding transformer, three chains (NTC → bridge → C → regulator): discrete 15 V, LM317 15 V, 7805 5 V.
- ±20 % mains gives V_C ≈ 27–40 V, so Q1 sees 12–25 V across it: size the heat sink for the high-mains corner.
- R5 protects the op-amp (worst case: shorted output); a resistor + zener gives the op-amp a steady supply.
- LM317: V₀ = 1.25 (1 + R2/R1). LM723 is the discrete design in one IC. 78xx: fixed, three pins, no extra parts.
- Every IC regulator needs > 3 V headroom at the ripple valley and a heat sink; verify with line and load regulation plots.

## Sources
- Video: "W1_L1.6: Example – linear power supply", IIT Madras BS in Electronic Systems: https://www.youtube.com/watch?v=uUPryFq32oY (backbone of all content).
- Texas Instruments, LM317 datasheet (SLVS044Z): https://www.ti.com/lit/ds/symlink/lm317.pdf (V₀ = V_REF(1 + R2/R1) + I_ADJ·R2, I_ADJ ≈ 50 µA, R1 = 240 Ω typical, thermal table and the heat-sink equation θ_HA ≤ θ_JA − (θ_CH + θ_JC)).
- Texas Instruments, LM340 / LM78xx datasheet: https://www.ti.com/lit/ds/symlink/lm7800.pdf (1.5 A, 35 V max input, ≈ 2 V dropout at 1 A, 3–15 V output options).
- Previous briefs in this folder set: `lectures/full-bridge-linear-regulator/` and `lectures/linear-power-supply/` (the discrete regulator, foldback and NTC this lecture assembles).
