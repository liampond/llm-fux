# Evaluation Criteria for LLM-Generated Species Counterpoint

Manual assessment framework for comparing three LLMs (ChatGPT, Claude, Gemini)
on Fux-based species counterpoint exercises.

---

## 1. Rule Compliance (Hard Constraints)

Binary pass/fail or violation count. These are directly verifiable against the
operational guides.

### 1A. Universal Rules (all species)

| #   | Criterion                              | Check | Scoring |
| --- | -------------------------------------- | ----- | ------- |
| U1  | **Opening interval**                   | First sounding note is a perfect consonance (unison, P5, P8) | Pass / Fail |
| U2  | **Opening rest**                       | Rest present only where the species permits it (allowed in 2nd species; forbidden in 1st, 3rd) | Pass / Fail |
| U3  | **Final note value**                   | Last measure is a single whole note | Pass / Fail |
| U4  | **Final interval**                     | Last note forms unison or octave with CF | Pass / Fail |
| U5  | **Parallel 5ths**                      | No parallel perfect 5ths between any adjacent structural beats | Count violations |
| U6  | **Parallel 8ths**                      | No parallel octaves between any adjacent structural beats | Count violations |
| U7  | **Hidden (direct) 5ths / 8ths**       | Similar motion into a perfect consonance only if the upper voice moves by step | Count violations |
| U8  | **Ottava battuta**                     | No contrary stepwise approach to an octave from a 10th | Count violations |
| U9  | **Voice crossing**                     | Voices do not cross (or cross only briefly where the species guide permits it) | Count violations |
| U10 | **Spacing ≤ 10th**                     | Vertical interval never exceeds a 10th at any sounding moment | Count violations |
| U11 | **Cadential accidental**               | Correct accidental applied per the final-note table (D → C#, G → F#, A → G#; none for C, E, F) | Pass / Fail |
| U12 | **Unison avoidance**                   | Unisons appear only at first and last measures, never mid-exercise | Count violations |
| U13 | **Leap compensation**                  | Every melodic leap > 3rd is immediately followed by stepwise contrary motion | Count violations |
| U14 | **Forbidden melodic intervals**        | No augmented, diminished, or chromatic melodic intervals; no major 6th; no descending minor 6th; nothing larger than an octave | Count violations |
| U15 | **Tritone prohibition (mi contra fa)** | No vertical tritone, no melodic tritone leap, no outlined tritone (unless resolved by continuation through it) | Count violations |
| U16 | **Melodic range**                      | Total span of the counterpoint line ≤ 10th | Pass / Fail |
| U17 | **Modal integrity**                    | No chromatic alterations except the mandatory cadential inflection | Count violations |
| U18 | **Imperfect consonance preference**    | More imperfect than perfect consonances in the interior; no more than three consecutive same-type imperfect consonances (three 3rds, three 6ths, or three 10ths) | Pass / Fail |
| U19 | **Motion category progression**        | Perfect → Perfect: only contrary/oblique. Imperfect → Perfect: only contrary/oblique. Other transitions: any motion permitted | Count violations |

### 1B. Species-Specific Rules

#### 1st Species (1:1)

| #    | Criterion                         | Check |
| ---- | --------------------------------- | ----- |
| S1-1 | **Note-against-note consonance**  | Every note forms a consonance with the CF |
| S1-2 | **Pitch repetition (oblique motion)** | Same pitch may appear up to 3 times consecutively (two repetitions), provided the vertical interval against the CF changes at each repetition. More than 3 consecutive appearances are forbidden. This is the only form of oblique motion in 1st species; it preserves singability by preventing excessive melodic motion |
| S1-3 | **Cadence — CP above CF**         | Penultimate bar is a major 6th resolving outward to octave by contrary motion |
| S1-4 | **Cadence — CP below CF**         | Penultimate bar is a minor 3rd resolving inward to unison by contrary motion |
| S1-5 | **Unison approach**               | No leap into or out of a unison except at the very beginning or end |

#### 2nd Species (2:1)

| #    | Criterion                        | Check |
| ---- | -------------------------------- | ----- |
| S2-1 | **Downbeat consonance**          | Every downbeat (Beat 1) is consonant |
| S2-2 | **Upbeat dissonance treatment**  | Beat 2 is dissonant ONLY as a passing tone (approached and left by step in the same direction) |
| S2-3 | **Opening half-rest**            | Exercise begins with a half rest followed by a half note (if required by guide version) |
| S2-4 | **Penultimate approach**         | Correct approach to the cadence via the penultimate upbeat |

#### 3rd Species (4:1)

| #    | Criterion                                  | Check |
| ---- | ------------------------------------------ | ----- |
| S3-1 | **Beat 1 consonance**                      | Every Beat 1 is consonant |
| S3-2 | **Beat 2 dissonance**                      | Dissonant only as a passing tone (step in, step out, same direction) |
| S3-3 | **Beat 3 dissonance — four-note scalar rule** | Dissonant on Beat 3 ONLY if part of a unidirectional 4-note scale AND Beats 2 & 4 are consonant; otherwise Beat 3 must be consonant |
| S3-4 | **Beat 4 dissonance**                      | Dissonant only as a passing tone resolving to the next consonant downbeat |
| S3-5 | **Nota Cambiata correctness**              | If used: exact 5-note pattern (cons → diss step down → cons leap 3rd down → cons step up → cons step up) |
| S3-6 | **Cambiata interval pattern**              | Above CF: 8-7-5-6 \| 8. Below CF: 3-4-6-5 \| 1 |
| S3-7 | **Cambiata not repeated**                  | Cambiata not used multiple times consecutively |
| S3-8 | **Structural reduction (T1–T3)**           | No parallel 5ths/8ths between Beat 1 and Beat 3 of successive measures |
| S3-9 | **Syncopated parallel (T4–T1)**            | Beat 4 of measure A does not form the same perfect interval as Beat 1 of measure B |
| S3-10| **Cadence target interval**                | Beat 4 of penultimate measure is Maj 6th (above) or min 3rd (below) |

#### 4th Species (Syncopation)

| #    | Criterion                        | Check |
| ---- | -------------------------------- | ----- |
| S4-1 | **Suspension preparation**       | Every dissonance is prepared as a consonance on the preceding weak beat |
| S4-2 | **Suspension resolution**        | Every dissonance resolves downward by step to a consonance |
| S4-3 | **Correct suspension types**     | Only permitted suspensions used (7–6, 4–3 above; 2–3, 9–10 below, etc.) |
| S4-4 | **Breaking the syncopation**     | If the chain breaks, the break follows the guide's rules (consonant half notes) |
| S4-5 | **Re-entering syncopation**      | After a break, the syncopation resumes correctly |

#### 5th Species (Florid)

| #    | Criterion                          | Check |
| ---- | ---------------------------------- | ----- |
| S5-1 | **Rhythmic variety**               | Mix of whole, half, and quarter notes (not just one value dominating) |
| S5-2 | **Quarter notes in pairs**         | Quarter notes appear in groups of 2 or 4, not isolated |
| S5-3 | **Suspension usage**               | At least some tied suspensions are present (florid ≠ just 3rd species) |
| S5-4 | **Species integration**            | The exercise convincingly combines techniques from species 1–4 |
| S5-5 | **Pitch repetition**               | Immediate pitch repetition forbidden except for the ornamental resolution of a syncopation (repeated pitch between beats 2 and 3 as part of the prescribed ornamental figure) |
| S5-6 | **Eighth notes**                   | Only permitted as a pair on Beat 4 resolving to the next downbeat (if the guide allows them at all) |

### 1C. Violation Severity Weighting

| Severity | Weight | Examples |
| -------- | ------ | -------- |
| **Critical** | ×3 | Parallel 5ths/8ths, wrong final interval, unprepared/unresolved dissonance, wrong cadential accidental |
| **Major**    | ×2 | Spacing > 10th, incorrect cambiata pattern, wrong beat consonance/dissonance, hidden 5ths/8ths, modal integrity violation, forbidden melodic interval |
| **Minor**    | ×1 | Leap compensation missing, voice crossing, unison mid-exercise, imperfect consonance balance, ottava battuta |

**Rule Compliance Score = Σ (violation count × severity weight).** Lower is better.

---

## 2. Musical Quality (Expert Assessment)

Likert scale 1–5, assessed by the evaluator as domain expert.

| Score | Meaning |
| ----- | ------- |
| 1     | Poor — fundamentally unmusical or incoherent |
| 2     | Weak — technically passable but clearly flawed |
| 3     | Adequate — what a mediocre student would produce |
| 4     | Good — competent, musical, minor quibbles only |
| 5     | Excellent — could appear in a Fux textbook as an example |

### 2A. Melodic Quality of the Counterpoint Line

| #  | Criterion                  | Description |
| -- | -------------------------- | ----------- |
| M1 | **Contour & arch**         | Does the melody have a clear overall shape — a single climax point, placed neither at the very beginning nor at the very end? Or is the line flat, aimless, or erratic? |
| M2 | **Stepwise predominance**  | Is the line predominantly conjunct (stepwise), with leaps used sparingly for contrast and energy? |
| M3 | **Leap quality & placement** | Are leaps well-chosen (varied interval sizes, not always the same)? Do they occur at musically logical points — to create a climax, to change register, to renew energy? |
| M4 | **Range utilisation**       | Does the line explore a reasonable portion of its available range (roughly an octave to a 10th), or does it huddle in a narrow band / needlessly sprawl? |
| M5 | **Avoidance of monotony**  | Does the melody avoid immediate pitch repetition (in species 2–5), mechanical sequential patterns, and aimless oscillation between two pitches? In 1st species: is pitch repetition used purposefully (with changing vertical intervals) rather than as a crutch? |
| M6 | **Singability**            | Could a singer perform this line naturally? No awkward interval successions, no disorienting chains of direction changes, no sense of being "generated" rather than "composed"? |

### 2B. Contrapuntal Relationship (Between the Two Voices)

| #  | Criterion                    | Description |
| -- | ---------------------------- | ----------- |
| C1 | **Motion variety**           | Good balance of contrary, oblique, and similar motion — not just one type throughout |
| C2 | **Intervallic variety**      | Uses a range of consonances (3rds, 6ths, 5ths, 8ths, 10ths) — not locked into parallel thirds or sixths the whole time |
| C3 | **Independence of voices**   | The counterpoint has its own melodic identity — its own climax, its own rhythm of tension and repose — rather than simply shadowing the CF |
| C4 | **Tension & release**        | Moments of tension (dissonance in species 2–5, contrary motion, narrowing/widening intervals) are balanced by moments of resolution and consonant stability |
| C5 | **Cadential convincingness** | The cadence feels like a genuine arrival — the penultimate measure creates directed motion toward the final, not just a mechanical landing on the correct interval |
| C6 | **Oblique motion quality (1st species)** | When pitch repetition (oblique motion) is used, does it serve the musical line — providing repose, preventing excessive motion, allowing the CF to "move around" the held pitch — or does it feel like the LLM ran out of ideas? |

### 2C. Stylistic Appropriateness

| #  | Criterion                        | Description |
| -- | -------------------------------- | ----------- |
| A1 | **Modal coherence**              | The counterpoint sounds like it belongs in the given mode — the character of the mode (Dorian gravity, Mixolydian brightness, etc.) is audible, not neutralised |
| A2 | **Period-appropriate character**  | Sounds like Renaissance-era pedagogical counterpoint, not Romantic harmony, jazz voice-leading, or modern parallel motion |
| A3 | **Pedagogical plausibility**     | Would this exercise be credible as student work submitted to Fux? Not too simplistic (just oscillating 3rds), not suspiciously clever (complex patterns an LLM shouldn't "know") |

### 2D. Scoring

- **Melodic Quality** = average of M1–M6
- **Contrapuntal Quality** = average of C1–C6
- **Stylistic Quality** = average of A1–A3
- **Overall Musical Quality** = (40% × Melodic) + (40% × Contrapuntal) + (20% × Stylistic)

---

## 3. Output Format & Parsability

| #  | Criterion               | Check | Scoring |
| -- | ----------------------- | ----- | ------- |
| F1 | **Valid MusicXML**       | Does the output parse without errors? | Pass / Fail |
| F2 | **Correct encoding**    | Right clefs, key signatures, time signatures, note durations | Count errors |
| F3 | **Part assignment**     | CF and counterpoint correctly placed in the right voices | Pass / Fail |
| F4 | **Completeness**        | All measures present; no truncation or hallucinated extra bars | Pass / Fail |

---

## 4. Prompt Adherence & Consistency

| #  | Criterion                   | Check | Scoring |
| -- | --------------------------- | ----- | ------- |
| P1 | **Instruction following**   | Did the LLM respect the species, the CF, the voice position (above/below)? | Pass / Fail |
| P2 | **Consistency across runs** | Given the same prompt multiple times, how stable is the quality? | Variance of scores across runs |
| P3 | **Self-correction ability** | If the LLM explains its reasoning, does the reasoning match the actual output? | Pass / Fail |
| P4 | **Hallucination rate**      | Does the LLM invent rules not in the guide, misstate rules, or claim its output satisfies rules that it violates? | Count instances |

---

## Summary Scorecard

| Category                | Sub-category              | Metric type                      | Weight |
| ----------------------- | ------------------------- | -------------------------------- | ------ |
| **Rule Compliance**     | Universal rules (U1–U19)  | Weighted violation count         | 25%    |
|                         | Species-specific rules    | Weighted violation count         | 25%    |
| **Musical Quality**     | Melodic (M1–M6)          | Likert 1–5 average              | 20%    |
|                         | Contrapuntal (C1–C6)     | Likert 1–5 average              | 15%    |
|                         | Stylistic (A1–A3)        | Likert 1–5 average              | 10%    |
| **Output Format**       | F1–F4                    | Pass/Fail + error count          | 5%     |

The 50/50 split between rule compliance and musical quality reflects that in
species counterpoint pedagogy, following the rules *is* the craft — but what
separates a good exercise from a merely correct one is the musical dimension.
