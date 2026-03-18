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
| U1  | **Opening interval**                   | First sounding note is a perfect consonance (unison, P5, P8). P5 only permitted when counterpoint is above CF. | Pass / Fail |
| U2  | **Opening rest**                       | Rest present only where the species permits it (allowed in 2nd, 4th, 5th species; forbidden in 1st, 3rd) | Pass / Fail |
| U3  | **Final note value**                   | Last measure is a single whole note | Pass / Fail |
| U4  | **Final interval**                     | Last note forms unison or octave with CF | Pass / Fail |
| U5  | **Penultimate approach**               | Correct approach to the cadence in the penultimate measure per the species-specific formulation in the guide (see species-specific cadence criteria S1-3/S1-4, S2-4, S3-10, S4-12, S5-16) | Pass / Fail |
| U6  | **Parallel 5ths**                      | No parallel perfect 5ths between any adjacent structural beats | Count |
| U7  | **Parallel 8ths**                      | No parallel octaves between any adjacent structural beats | Count |
| U8  | **Hidden (direct) 5ths / 8ths**       | Similar motion into a perfect consonance only if the upper voice moves by step | Count |
| U9  | **Ottava battuta**                     | No contrary stepwise approach to an octave from a 10th | Count |
| U10 | **Voice crossing**                     | Voices do not cross (or cross only briefly where the species guide permits it). 3rd species: must resolve within 3 quarter notes. 4th species: only if consonant syncopation, must leap out immediately. | Count |
| U11 | **Spacing ≤ 10th**                     | Vertical interval never exceeds a 10th at any sounding moment. Exception: in 4th/5th species, a consonant syncopation may produce up to a 12th on the downbeat if the counterpoint immediately leaps back within a 10th on the following note. The preparation (beat 3 / upbeat) must ALWAYS be ≤ 10th without exception. | Count |
| U12 | **Cadential accidental**               | Correct accidental applied per the final-note table (D → C#, G → F#, A → G#; none for C, E, F) | Pass / Fail |
| U13 | **Forbidden melodic intervals**        | No augmented, diminished, or chromatic melodic intervals; no major 6th; no descending minor 6th; nothing larger than an octave | Count |
| U14 | **Tritone prohibition (mi contra fa)** | No vertical tritone, no melodic tritone leap, no outlined tritone (unless resolved by continuation through it). Exception: diminished 5th permitted on beat 3 of the penultimate measure in cadential context (3rd/5th species above CF). | Count |
| U15 | **Melodic range**                      | Total span of the counterpoint line ≤ 10th | Pass / Fail |
| U16 | **Modal integrity**                    | No chromatic alterations except: (a) the mandatory cadential inflection (D/C#, G/F#, A/G#), and (b) Bb when CF is in F (see U18) | Count |
| U17 | **Motion category progression**        | Perfect → Perfect: only contrary/oblique. Imperfect → Perfect: only contrary/oblique. Other transitions: any motion permitted | Count |
| U18 | **Bb rule (CF in F)**                  | When CF is in F (Lydian), B must be lowered to Bb wherever it creates a melodic tritone with F — either as a direct leap (F–B or B–F) or as the boundary of a stepwise passage (F–G–A–B or B–A–G–F). Not a blanket substitution: only where B participates in a tritone relationship with F. | Count |
| U19 | **Leap compensation**                  | Every melodic leap > 3rd must be immediately followed by stepwise motion in the opposite direction | Count |
| U20 | **Legit dissonances**                  | Every dissonance must fit the requirements of the active species logic. A dissonance not derivable from any licensed treatment (passing tone, suspension, cambiata, four-note scalar rule) is an error. | Count |

### 1B. Species-Specific Rules

#### 1st Species (1:1)

| #    | Criterion                             | Check | Scoring |
| ---- | ------------------------------------- | ----- | ------- |
| S1-1 | **Note-against-note consonance**      | Every note forms a consonance with the CF | Count |
| S1-2 | **Pitch repetition (oblique motion)** | Same pitch may appear up to 3 times consecutively (two repetitions), provided the vertical interval against the CF changes at each repetition. More than 3 consecutive appearances are forbidden. | Count |
| S1-3 | **Cadence — CP above CF**             | Penultimate bar is a major 6th resolving outward to octave by contrary motion | Pass / Fail |
| S1-4 | **Cadence — CP below CF**             | Penultimate bar is a minor 3rd resolving inward to unison by contrary motion | Pass / Fail |
| S1-5 | **Unison approach**                   | No leap into or out of a unison except at the very beginning or end. A unison reached by step from a 3rd by contrary motion is also to be avoided in the interior. | Count |
| S1-6 | **Unison avoidance**                  | Unisons appear only at first and last measures, never mid-exercise | Count |
| S1-7 | **Imperfect consonance preference**   | More imperfect than perfect consonances in the interior; no more than three consecutive same-type imperfect consonances (three 3rds, three 6ths, or three 10ths) | Pass / Fail |

#### 2nd Species (2:1)

| #    | Criterion                            | Check | Scoring |
| ---- | ------------------------------------ | ----- | ------- |
| S2-1 | **Downbeat consonance**              | Every downbeat (Beat 1 / Thesis) is consonant | Count |
| S2-2 | **Upbeat dissonance treatment**      | Upbeat (Beat 3 / Arsis) is dissonant ONLY as a passing tone: approached and left by step in the same direction, filling a 3rd between two consonant downbeats | Count |
| S2-3 | **Opening half-rest**                | Exercise begins with a half rest on the downbeat followed by a half note on the upbeat | Pass / Fail |
| S2-4 | **Penultimate cadence formula**      | CP above: Thesis = P5, Arsis = M6 → final octave. CP below: Thesis = 5th, Arsis = m3 → final unison. When the diatonic 5th on the thesis is diminished (e.g., penultimate CF = B), apply accidental to produce P5. | Pass / Fail |
| S2-5 | **Downbeat parallel (Thesis→Thesis)**| No parallel P5 or P8 between consecutive downbeats. If a parallel exists, it is mitigated only if the intervening upbeat moves by a leap ≥ 4th (the "Leap Rule"). An upbeat a 3rd away does NOT break the parallel. | Count |
| S2-6 | **Cross-barline parallel (Arsis→Thesis)** | The upbeat of measure N and the downbeat of measure N+1 must not both form P5, or both form P8, with their respective CF notes. Check at every barline. | Count |
| S2-7 | **Cross-barline pitch repetition**   | The upbeat pitch of measure N must not be identical to the downbeat pitch of measure N+1. A repeated pitch across the barline creates stagnant motion. | Count |
| S2-8 | **Unison restriction**               | Unison on the downbeat (Thesis) is permitted almost only in first and last measures. A unison on the upbeat (Arsis) is acceptable but must be extremely rare: at most one per exercise. | Count |

#### 3rd Species (4:1)

| #     | Criterion                                  | Check | Scoring |
| ----- | ------------------------------------------ | ----- | ------- |
| S3-1  | **Beat 1 consonance**                      | Every Beat 1 is consonant | Count |
| S3-2  | **Beat 2 dissonance**                      | Dissonant only as a passing tone (step in, step out, same direction) | Count |
| S3-3  | **Beat 3 dissonance — four-note scalar rule** | Dissonant on Beat 3 ONLY if part of a unidirectional 4-note scale AND Beats 2 & 4 are consonant; if the melody changes direction at Beat 3, it MUST be consonant | Count |
| S3-4  | **Beat 4 dissonance**                      | Dissonant only as a passing tone resolving to the next consonant downbeat by step | Count |
| S3-5  | **Nota Cambiata correctness**              | If used: exact 5-note pattern (consonant → dissonant step down → consonant leap 3rd down → consonant step up → consonant step up). The figure starts on Beat 1 or Beat 3. | Count |
| S3-6  | **Cambiata interval pattern**              | Above CF: 8-7-5-6 \| 8. Below CF: 3-4-6-5 \| 1. | Pass / Fail |
| S3-7  | **Cambiata not repeated**                  | Cambiata not used multiple times consecutively | Count |
| S3-8  | **Structural reduction (T1–T3)**           | Extract Beat 1 and Beat 3 of every measure. No parallel 5ths/8ths in this reduction. | Count |
| S3-9  | **Cross-barline parallel (T4–T1)**         | Beat 4 of measure N and Beat 1 of measure N+1 must not both form P5, or both form P8, with their respective CF notes. Check at every barline. | Count |
| S3-10 | **Cadence target interval**                | Beat 4 of penultimate measure is M6 (CP above) or m3 (CP below). Stepwise formula above: 3-4-5-6 \| 8. Cambiata option above: 8-7-5-6 \| 8. Stepwise below variant 1: 3-5-4-3 \| 1. Stepwise below variant 2: 6-3-6-3 \| 1. Cambiata below: 3-4-6-5 \| 1. | Pass / Fail |
| S3-11 | **Unison exception (beat 2 only)**         | Unison is permitted only in first/last measures, with one narrow exception: on Beat 2 only, within a licensed pattern, max once per exercise. Below CF: 8-1-3-4, 3-1-3, 5-1-3. Above CF: 3-1-3-4. Outside these patterns, unison is forbidden. | Count |
| S3-12 | **Cross-barline motion (beat 4 → beat 1)** | Default motion from Beat 4 to the following Beat 1 is conjunct (stepwise). Leaps across the barline are strongly discouraged. The one licensed leap exception: step-step-3rd down from beats 1-2-3, then leap from Beat 4 to a consonant Beat 1. This figure must not recur within the same exercise. | Count |

#### 4th Species (Syncopation)

| #     | Criterion                            | Check | Scoring |
| ----- | ------------------------------------ | ----- | ------- |
| S4-1  | **Suspension preparation**           | Every dissonance is prepared as a consonance on the preceding weak beat (arsis). No dissonance is permitted at the preparation stage. | Count |
| S4-2  | **Suspension resolution**            | Every dissonant suspension resolves DOWNWARD by step to a consonance. Upward resolution of a dissonance is strictly forbidden. | Count |
| S4-3  | **Correct suspension types (CF below, CP above)** | Only 7-6, 4-3, 9-8 permitted. The 9-8 must NOT be prepared by an octave (8-9-8 = hidden octaves in reduction, forbidden). The 2-1 (CP steps down to unison) is admissible at most once per exercise and only when no other continuation is available. | Count |
| S4-4  | **Correct suspension types (CF above, CP below)** | Only 2-3, 4-5, 9-10 permitted. The 7-8 suspension is excluded by convention. | Count |
| S4-5  | **Breaking the syncopation**         | If the chain breaks, the break consists of two untied consonant half notes. The syncopation must resume in the following measure. | Count |
| S4-6  | **Re-entering syncopation**          | After a break, the syncopation resumes correctly on the next available arsis. | Count |
| S4-7  | **Reduction validity**               | Remove all ties and treat syncopated notes as direct attacks on the downbeat. The resulting 1:1 framework must not contain parallel unisons (1-1), parallel fifths (5-5), or parallel octaves (8-8). | Count |
| S4-8  | **Unison on thesis forbidden**       | Unison on the downbeat (thesis) is permitted only in the final measure. | Count |
| S4-9  | **Unison pivot (CF above, CP below)**| If a unison appears on the arsis as a pivot to restart a broken chain, it must be strictly because a 3rd on the thesis blocked the chain, and it must be followed immediately by a thesis half note leading back into syncopation. Extremely rare — last resort only. | Count |
| S4-10 | **Consonant syncopation freedom**    | If the tied note forms a consonance on the downbeat, it may proceed by step (up or down) or leap to another consonance — no obligatory downward resolution. Verify that no consonant syncopation is incorrectly resolved as if dissonant. | Pass / Fail |
| S4-11 | **Opening half-rest**                | Exercise begins with a half rest on the downbeat, first sounding note on the arsis forming a perfect consonance (1, 5, 8). | Pass / Fail |
| S4-12 | **Penultimate cadence formula**      | CP above (CF below): 7-6 suspension — 7th on downbeat prepared by consonant arsis in antepenultimate, tied; M6 resolution on arsis → octave in final. CP below (CF above): 2-3 suspension — 2nd on downbeat, m3 resolution on arsis → unison in final. Cadential accidental applies to the resolution note. | Pass / Fail |

#### 5th Species (Florid)

| #     | Criterion                                 | Check | Scoring |
| ----- | ----------------------------------------- | ----- | ------- |
| S5-1  | **Rhythmic variety**                      | Mix of whole, half, quarter notes, and tied syncopations. No single texture should dominate for more than two consecutive measures. The exercise should feel like a continuous melodic line changing its rhythmic character often. | Pass / Fail |
| S5-2  | **Suspension usage**                      | At least some tied suspensions present. Florid counterpoint ≠ just 3rd species writing. When the CF permits consecutive suspensions, a syncopation chain is preferred (§V.F of 5th species guide). | Pass / Fail |
| S5-3  | **Species integration**                   | The exercise convincingly combines techniques from species 1–4: whole-note moments, half-note pairs, quarter-note passages, and tied syncopations all appear. | Pass / Fail |
| S5-4  | **Pitch repetition**                      | Immediate pitch repetition forbidden except in the ornamental resolution of a syncopation (licensed repetition between beats 2 and 3 in the 7-6-6 or 2-3-3 patterns of §V.E). | Count |
| S5-5  | **Eighth notes — beat placement**         | Eighth notes may ONLY appear on beats 2 and 4. Strictly forbidden on beats 1 and 3. No groupings of four consecutive eighth notes. | Count |
| S5-6  | **Eighth notes — licensed contexts only** | Eighth notes are permitted only as: (a) ornamented accent, (b) ornamented anticipation, (c) scalar gap fill (§VI.C), or (d) ornamented resolution (§VI.D). Each context has specific interval patterns per CF position (above/below). | Count |
| S5-7  | **P4 check (below CF)**                   | When counterpoint is below the CF, every note must be checked against the forbidden P4 pitch table. A P4 is dissonant even when the counterpoint is the lower voice. P4 on beat 1 or 3 is forbidden unless it is a valid tied suspension. | Count |
| S5-8  | **Dissonant half note on beat 3**         | A half note on beat 3 follows second-species logic and MUST be consonant. A dissonant half note on beat 3 is NEVER permitted. Only a dissonant quarter note on beat 3 is valid (as part of a four-quarter-note passage under the third-species scalar rule). | Count |
| S5-9  | **Half note on beats 2 / 4 forbidden**    | A half note starting on beat 2 or beat 4 is strictly forbidden in 5th species (second-species logic restricts half notes to beats 1 and 3). Similarly, a quarter note on beat 4 tied across the barline to a quarter note on beat 1 of the following measure is forbidden: it produces a displaced half-note effect equivalent to a half note starting on beat 4. The only valid cross-barline tie is the fourth-species ligature (half note on beat 3 tied to beat 1). | Count |
| S5-10 | **Consonant mediation patterns**          | If a 7-3-6 (above) or 2-6-3 (below) pattern is used: the mediation note on beat 2 must be consonant with CF, the downward leap from the suspension must not exceed a P5, and the leap must not form a melodic tritone. Under reduction, the suspension still resolves to the resolution interval on beat 3. | Count |
| S5-11 | **Resolution repetition patterns**        | If a 7-6-6 (above) or 2-3-3 (below) pattern is used: the pitch repetition between beats 2 and 3 is the licensed exception. Valid only in this ornamental context; preferred in the antepenultimate measure. | Count |
| S5-12 | **Ornamented resolution patterns**        | If an ornamented resolution is used (7-(6-5)-6, 4-(3-2)-3 above; 2-(3-4)-3, 4-(5-6)-5 below): the eighth-note pair on beat 2 must be strictly conjunct and diatonic. The structural resolution falls on beat 3. Under reduction, the suspension resolves directly to the beat 3 interval. | Count |
| S5-13 | **Scalar gap fill patterns**              | If eighth notes fill a melodic third-gap: CF below (above): ascending 5-[6-7]-8 on beats 1-2-3 only (eighth pair on beat 2); descending 3-[5-4]-3 on beats 1-2-3 or 3-4-1. CF above (below): 6-[8-7]-6 or 3-[5-4]-3 on beats 1-2-3 or 3-4-1. Eighths must be diatonic and conjunct. | Count |
| S5-14 | **Cross-barline parallel (last note → beat 1)** | The last sounding note of each measure and the first sounding note of the following measure must not both form P5, or both form P8, with their respective CF notes. Check at every barline regardless of rhythmic value. | Count |
| S5-15 | **No more than two consecutive free half notes** | In 5th species, Fux does not use more than two distinct half notes in succession (second-species logic). A third consecutive untied half note is a violation. | Count |
| S5-16 | **Penultimate must use syncopated cadence** | The penultimate measure MUST use a syncopated cadential suspension (not optional). CP above: 7-6 (M6 resolution → octave). CP below: 2-3 (m3 resolution → unison). The suspension is prepared by a consonant half note on beat 3 of the antepenultimate measure. Cadential accidental applied to the resolution note. | Pass / Fail |
| S5-17 | **Half-note frequency (stylistic)**       | Half notes must be used less frequently than quarter notes and syncopations (ornamented or not) combined. In Fux's florid style, quarter-note motion and tied syncopations are the normative rhythmic values; half notes serve only as structural punctuation (preparation notes, isolated stable moments) and must not dominate the texture. An exercise where half notes outnumber or equal quarter notes + syncopations lacks the flowing character that defines the fifth species. | Count |

### 1C. Violation Severity Weighting

| Severity     | Weight | Examples |
| ------------ | ------ | -------- |
| **Critical** | ×3     | Parallel 5ths/8ths (U6/U7), wrong final interval (U4), unprepared dissonance (S4-1/U20), unresolved dissonance (S4-2), wrong cadential accidental (U12), P4 on strong beat below CF (S5-7), reduction reveals parallels (S4-7) |
| **Major**    | ×2     | Spacing > 10th (U11), hidden 5ths/8ths (U8), wrong beat consonance/dissonance (S3-1 through S3-4, S5-8), modal integrity violation (U16), forbidden melodic interval (U13), incorrect suspension type (S4-3/S4-4), cross-barline parallel (S2-6, S3-9, S5-14), wrong cadence formula (U5) |
| **Minor**    | ×1     | Leap compensation missing (U19), voice crossing (U10), unison mid-exercise (S1-6), imperfect consonance balance (S1-7), ottava battuta (U9), cross-barline pitch repetition (S2-7), cross-barline leap (S3-12), cambiata repeated (S3-7), no rhythmic variety (S5-1), half-note preponderance (S5-17) |

**Rule Compliance Score = Σ (violation count × severity weight).** Lower is better.

---

## 2. Musical Quality (Expert Assessment)

Likert scale 1–5, assessed by the evaluator as domain expert.

| Score | Meaning      | Description |
| ----- | ------------ | ----------- |
| 1     | Poor         | Fundamentally unmusical or incoherent |
| 2     | Weak         | Technically passable but clearly flawed |
| 3     | Adequate     | What a mediocre student would produce |
| 4     | Good         | Competent, musical, minor quibbles only |
| 5     | Excellent    | Could appear in a Fux textbook as an example |

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
| P5 | **Originality of the solution** | Does the LLM generate an original solution each time, without reproducing the same or a very similar output across successive generations? | Count instances |

---

## Summary Scorecard

| Category                | Sub-category              | Metric type                      | Weight |
| ----------------------- | ------------------------- | -------------------------------- | ------ |
| **Rule Compliance**     | Universal rules (U1–U20)  | Weighted violation count         | 25%    |
|                         | Species-specific rules    | Weighted violation count         | 25%    |
| **Musical Quality**     | Melodic (M1–M6)          | Likert 1–5 average              | 20%    |
|                         | Contrapuntal (C1–C6)     | Likert 1–5 average              | 15%    |
|                         | Stylistic (A1–A3)        | Likert 1–5 average              | 10%    |
| **Output Format**       | F1–F4                    | Pass/Fail + error count          | 5%     |

The 50/50 split between rule compliance and musical quality reflects that in
species counterpoint pedagogy, following the rules *is* the craft — but what
separates a good exercise from a merely correct one is the musical dimension.
