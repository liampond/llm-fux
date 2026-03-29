# Evaluation of CAMBIATA (Counterpoint and MusicXML By Instructing AI Through APIs)

## Assessment Framework

Comparing ChatGPT, Claude, and Gemini on Fux-Based Species Counterpoint Exercises

---

# 1. Rule Compliance (Hard Constraints)

Binary pass/fail or violation count. These criteria are directly verifiable against the operational guides.

## 1A. Universal Rules (All Species)

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| U1 | Opening interval | First sounding note is a perfect consonance (unison, P5, P8). P5 only permitted when counterpoint is above CF. | Pass / Fail |
| U2 | Opening rest | Rest present only where the species permits it (allowed in 2nd, 4th, 5th species; forbidden in 1st, 3rd) | Pass / Fail |
| U3 | Final note value | Last measure is a single whole note | Pass / Fail |
| U4 | Final interval | Last note forms unison or octave with CF | Pass / Fail |
| U5 | Penultimate approach | Correct approach to the cadence in the penultimate measure per the species-specific formulation in the guide (see S1-3/S1-4, S2-4, S3-9, S4-11, S5-15) | Pass / Fail |
| U6 | Hidden (direct) 5ths / 8ths | Similar motion into a perfect consonance only if the upper voice moves by step | Count |
| U7 | Ottava battuta | No contrary stepwise approach to an octave from a 10th | Count |
| U8 | Voice crossing | Voices do not cross (or cross only briefly where permitted). 3rd species: must resolve within 3 quarter notes. 4th species: only if consonant syncopation, must leap out immediately. | Count |
| U9 | Spacing ≤ 10th | Vertical interval never exceeds a 10th at any sounding moment. Exception: in 4th/5th species, a consonant syncopation may produce up to a 12th on the downbeat if the counterpoint immediately leaps back within a 10th. The preparation must always be ≤ 10th. | Count |
| U10 | Cadential accidental | Correct accidental applied per the final-note table (D→C#, G→F#, A→G#; none for C, E, F) | Pass / Fail |
| U11 | Forbidden melodic intervals | No augmented, diminished, or chromatic melodic intervals; no major 6th; no descending minor 6th; nothing larger than an octave | Count |
| U12 | Tritone prohibition (mi contra fa) | No vertical tritone, no melodic tritone leap, no outlined tritone (unless resolved by continuation). Exception: diminished 5th permitted on beat 3 of penultimate measure in cadential context (3rd/5th species above CF). | Count |
| U13 | Melodic range | Total span of the counterpoint line ≤ 10th | Pass / Fail |
| U14 | Modal integrity | No chromatic alterations except: (a) the mandatory cadential inflection (D/C#, G/F#, A/G#), and (b) Bb when CF is in F (see U16) | Count |
| U15 | Motion category progression | Perfect→Perfect: only contrary/oblique. Imperfect→Perfect: only contrary/oblique. Other transitions: any motion permitted. | Count |
| U16 | Bb rule (CF in F) | When CF is in F (Lydian), B must be lowered to Bb wherever it creates a melodic tritone with F, either as a direct leap or as the boundary of a stepwise passage. Not a blanket substitution: only where B participates in a tritone relationship with F. | Count |
| U17 | Leap compensation | Every melodic leap > 3rd must be immediately followed by stepwise motion in the opposite direction | Count |
| U18 | Legit dissonances | Every dissonance must fit the requirements of the active species logic. A dissonance not derivable from any licensed treatment (passing tone, suspension, cambiata, four-note scalar rule) is an error. | Count |

## 1B. Species-Specific Rules

### 1st Species (1:1)

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| S1-1 | Note-against-note consonance | Every note forms a consonance with the CF | Count |
| S1-2 | Pitch repetition (oblique motion) | Same pitch may appear up to 3 times consecutively (two repetitions), provided the vertical interval against the CF changes at each repetition. More than 3 consecutive appearances are forbidden. | Count |
| S1-3 | Cadence (CP above CF) | Penultimate bar is a major 6th resolving outward to octave by contrary motion | Pass / Fail |
| S1-4 | Cadence (CP below CF) | Penultimate bar is a minor 3rd resolving inward to unison by contrary motion | Pass / Fail |
| S1-5 | Unison approach | No leap into or out of a unison except at the very beginning or end. A unison reached by step from a 3rd by contrary motion is also to be avoided in the interior. | Count |
| S1-6 | Unison avoidance | Unisons appear only at first and last measures, never mid-exercise | Count |
| S1-7 | Imperfect consonance preference | More imperfect than perfect consonances in the interior; no more than three consecutive same-type imperfect consonances (three 3rds, three 6ths, or three 10ths) | Pass / Fail |
| S1-8 | Parallel 5ths (thesis to thesis) | No parallel perfect 5ths between consecutive downbeats (beat 1 of measure N and beat 1 of measure N+1). Each pair of adjacent theses must be checked. | Count |
| S1-9 | Parallel 8ths (thesis to thesis) | No parallel octaves between consecutive downbeats (beat 1 of measure N and beat 1 of measure N+1). Each pair of adjacent theses must be checked. | Count |

### 2nd Species (2:1)

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| S2-1 | Downbeat consonance | Every downbeat (Beat 1 / Thesis) is consonant | Count |
| S2-2 | Upbeat dissonance treatment | Upbeat (Beat 3 / Arsis) is dissonant only as a passing tone: approached and left by step in the same direction, filling a 3rd between two consonant downbeats | Count |
| S2-3 | Opening half-rest | Exercise begins with a half rest on the downbeat followed by a half note on the upbeat | Pass / Fail |
| S2-4 | Penultimate cadence formula | CP above: Thesis = P5, Arsis = M6 → final octave. CP below: Thesis = 5th, Arsis = m3 → final unison. When the diatonic 5th on the thesis is diminished (e.g., penultimate CF = B), apply accidental to produce P5. | Pass / Fail |
| S2-5 | Downbeat parallel (Thesis→Thesis) | No parallel P5 or P8 between consecutive downbeats. If a parallel exists, it is mitigated only if the intervening upbeat moves by a leap ≥ 4th (the "Leap Rule"). An upbeat a 3rd away does not break the parallel. | Count |
| S2-6 | Cross-barline parallel (Arsis→Thesis) | The upbeat of measure N and the downbeat of measure N+1 must not both form P5, or both form P8, with their respective CF notes. Check at every barline. | Count |
| S2-7 | Cross-barline pitch repetition | The upbeat pitch of measure N must not be identical to the downbeat pitch of measure N+1. A repeated pitch across the barline creates stagnant motion. | Count |
| S2-8 | Unison restriction | Unison on the downbeat (Thesis) is permitted only in first and last measures. A unison on the upbeat (Arsis) is acceptable but must be rare: at most two per exercise. | Count |

### 3rd Species (4:1)

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| S3-1 | Beat 1 consonance | Every Beat 1 is consonant | Count |
| S3-2 | Beat 2 dissonance | Dissonant only as a passing tone (step in, step out, same direction) | Count |
| S3-3 | Beat 3 dissonance (four-note scalar rule) | Dissonant on Beat 3 only if part of a unidirectional 4-note scale and Beats 2 & 4 are consonant; if the melody changes direction at Beat 3, it must be consonant | Count |
| S3-4 | Beat 4 dissonance | Dissonant only as a passing tone resolving to the next consonant downbeat by step | Count |
| S3-5 | Nota Cambiata correctness | If used: exact 5-note pattern (consonant → dissonant step down → consonant leap 3rd down → consonant step up → consonant step up). The figure starts on Beat 1 or Beat 3. | Count |
| S3-6 | Cambiata interval pattern and non-repetition | Above CF: 8-7-5-6 \| 8. Below CF: 3-4-6-5 \| 1. The cambiata figure must not be used multiple times consecutively. | Count |
| S3-7 | Structural reduction (T1–T3) | Extract Beat 1 and Beat 3 of every measure. No parallel 5ths/8ths in this reduction. | Count |
| S3-8 | Cross-barline parallel (T4–T1) | Beat 4 of measure N and Beat 1 of measure N+1 must not both form P5, or both form P8, with their respective CF notes. Check at every barline. | Count |
| S3-9 | Cadence target interval | Beat 4 of penultimate measure is M6 (CP above) or m3 (CP below). Stepwise formula above: 3-4-5-6 \| 8. Cambiata option above: 8-7-5-6 \| 8. Stepwise below variant 1: 3-5-4-3 \| 1. Stepwise below variant 2: 6-3-6-3 \| 1. Cambiata below: 3-4-6-5 \| 1. | Pass / Fail |
| S3-10 | Unison exception (beat 2 only) | Unison is permitted only in first/last measures, with one narrow exception: on Beat 2 only, within a licensed pattern, max once per exercise. Below CF: 8-1-3-4, 3-1-3, 5-1-3. Above CF: 3-1-3-4. Outside these patterns, unison is forbidden. | Count |
| S3-11 | Cross-barline motion (beat 4 → beat 1) | Default motion from Beat 4 to the following Beat 1 is conjunct (stepwise). Leaps across the barline are not allowed, except for one licensed leap exception: step-step-3rd down from beats 1-2-3, then leap from Beat 4 to a consonant Beat 1. This figure must not recur within the same exercise. | Count |

### 4th Species (Syncopation)

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| S4-1 | Suspension preparation | Every dissonance is prepared as a consonance on the preceding weak beat (arsis). No dissonance is permitted at the preparation stage. | Count |
| S4-2 | Suspension resolution | Every dissonant suspension resolves downward by step to a consonance. Upward resolution of a dissonance is strictly forbidden. | Count |
| S4-3 | Correct suspension types (above) | Only 7-6 and 4-3 permitted as dissonant suspension types above the CF. | Count |
| S4-4 | 9-8 suspension restriction (above) | The 9-8 suspension is permitted only when the preparation is a 10th (10-9-8 pattern). A succession of 9-8 suspensions (9-8-9-8) produces parallel octaves in reduction and is forbidden. Preparation by an octave (8-9-8) equally constitutes hidden octaves and is not permitted. | Count |
| S4-5 | Correct suspension types (below) | Only 2-3, 4-5, 9-10 permitted. The 7-8 suspension is excluded by convention. The 2-1 is admissible at most once per exercise and only when no other continuation is available. | Count |
| S4-6 | Breaking and re-entering the syncopation | If the chain breaks, the break consists of two untied consonant half notes. The syncopation must resume correctly on the next available arsis in the following measure. | Count |
| S4-7 | Reduction validity | Remove all ties and treat syncopated notes as direct attacks on the downbeat. The resulting 1:1 framework must not contain parallel unisons (1-1), parallel fifths (5-5), or parallel octaves (8-8). | Count |
| S4-8 | Unison pivot (below CF) | If a unison appears on the arsis as a pivot to restart a broken chain, it must be strictly because a 3rd on the thesis blocked the chain, and it must be followed immediately by a thesis half note leading back into syncopation. Extremely rare. | Count |
| S4-9 | Consonant syncopation freedom | If the tied note forms a consonance on the downbeat, it may proceed by step (up or down) or leap to another consonance. No obligatory downward resolution. | Pass / Fail |
| S4-10 | Opening half-rest | Exercise begins with a half rest on the downbeat, first sounding note on the arsis forming a perfect consonance (1, 5, 8). | Pass / Fail |
| S4-11 | Penultimate cadence formula | CP above: 7-6 suspension (7th on downbeat prepared by consonant arsis in antepenultimate, tied; M6 resolution on arsis → octave in final). CP below: 2-3 suspension (2nd on downbeat, m3 resolution on arsis → unison in final). Cadential accidental applied to the resolution note. | Pass / Fail |

### 5th Species (Florid)

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| S5-1 | Texture diversity and species integration | The exercise must contain at least one instance of each of the following five rhythmic textures: (1) whole note (1st species), (2) half-note pair (2nd species), (3) quarter-note group of four (3rd species), (4) tied syncopation (4th species), (5) eighth-note pair. Count the number of distinct texture types present. An exercise that omits any of the five textures fails this criterion. Texture balance is further constrained by S5-7. | Count: N of 5 textures present |
| S5-2 | Suspension usage | At least 2 tied syncopations must be present and correctly used as prescribed by the 4th species suspension tables. Of these, at least one must be a dissonant syncopation and at least one must be a consonant syncopation. Fux characteristically uses consonant syncopations to create suspension that induce rhythmic diminution through scalar motion, introducing quarter notes on beats 2, 3, and 4. | Pass / Fail |
| S5-3 | Pitch repetition | Immediate pitch repetition forbidden except in the ornamental resolution of a syncopation (licensed repetition between beats 2 and 3 in the 7-6-6 or 2-3-3 patterns). | Count |
| S5-4 | Eighth notes (beat placement) | Eighth notes may only appear on beats 2 and 4. Strictly forbidden on beats 1 and 3. No groupings of four consecutive eighth notes. | Count |
| S5-5 | Eighth notes (licensed contexts) | Eighth notes are permitted only as: (a) ornamented accent, (b) ornamented anticipation, (c) scalar gap fill, or (d) ornamented resolution. Each context has specific interval patterns per CF position. | Count |
| S5-6 | P4 check (below CF) | When counterpoint is below the CF, every note must be checked against the forbidden P4 pitch table. A P4 is dissonant even when the counterpoint is the lower voice. P4 on beat 1 or 3 is forbidden unless it is a valid tied suspension or on beat 3 a passing note like in S3-3. | Count |
| S5-7 | Half-note frequency | 1. Half notes must be used less frequently than quarter notes and syncopations (ornamented or not) combined. The quarter note and the tied syncopation are the normative rhythmic values of the fifth species; half notes serve only as structural punctuation (preparation notes, isolated moments of stability) and must not dominate the texture. An exercise where half notes outnumber or equal quarter notes and syncopations lacks the flowing character that defines florid counterpoint. 2. Fux does not use more than two distinct half notes in succession; a third consecutive untied half note is a violation. | Count |
| S5-8 | Dissonant half note on beat 3 | A half note on beat 3 follows second-species logic and must be consonant. A dissonant half note on beat 3 is never permitted. Only a dissonant quarter note on beat 3 is valid (as part of a four-quarter-note passage under the third-species scalar rule). | Count |
| S5-9 | Half note on beats 2/4 and displaced half-note effects | A half note starting on beat 2 or beat 4 is strictly forbidden in 5th species (second-species logic restricts half notes to beats 1 and 3). A half note misplaced on beat 2 or 4 will render as two tied quarter notes, which is a clear notational sign of error. A quarter note on beat 4 tied across the barline to a quarter note on beat 1 of the following measure is equally forbidden: this figure creates a displaced half-note effect starting on beat 4, which is metrically equivalent to a half note on beat 4 and violates the same constraint. The only valid tie across the barline is the fourth-species ligature (a half note on beat 3 tied to beat 1). | Count |
| S5-10 | Consonant mediation patterns | If a 7-3-6 (above) or 2-6-3 (below) pattern is used: the mediation note on beat 2 must be consonant with CF, the downward leap from the suspension must not exceed a P5, and the leap must not form a melodic tritone. | Count |
| S5-11 | Resolution repetition patterns | If a 7-6-6 (above) or 2-3-3 (below) pattern is used: the pitch repetition between beats 2 and 3 is the licensed exception. Valid only in this ornamental context; preferred in the antepenultimate measure. | Count |
| S5-12 | Ornamented resolution patterns | If an ornamented resolution is used (7-(6-5)-6, 4-(3-2)-3 above; 2-(3-4)-3, 4-(5-6)-5 below): the eighth-note pair on beat 2 must be strictly conjunct and diatonic. The structural resolution falls on beat 3. | Count |
| S5-13 | Scalar gap fill patterns | If eighth notes fill a melodic third-gap: the pair must be diatonic and conjunct, placed on beats 2 or 4 only. Specific interval patterns per CF position apply. | Count |
| S5-14 | Parallel 5ths and 8ths (all textures) | Since 5th species combines all rhythmic textures, the model must first identify the rhythmic value of each note to determine which species logic governs the parallel check at any given point in the exercise. Whole-note passages (1st species logic): check for parallel 5ths and 8ths between consecutive theses (S1-8, S1-9). Half-note passages (2nd species logic): check thesis-to-thesis (S2-5) and arsis-to-thesis (S2-6). Quarter-note passages (3rd species logic): check structural reduction T1–T3 (S3-7) and cross-barline T4–T1 (S3-8). Syncopated passages (4th species logic): check the 1:1 reduction with ties removed (S4-7). Additionally, regardless of the active texture, the last sounding note of each measure and the first sounding note of the following measure must not both form P5, or both form P8, with their respective CF notes. Check at every barline. | Count |
| S5-15 | Penultimate syncopated cadence | The penultimate measure must use a syncopated cadential suspension (not optional). CP above: 7-6 (M6 resolution → octave). CP below: 2-3 (m3 resolution → unison). Suspension prepared by a consonant half note on beat 3 of the antepenultimate measure. Cadential accidental applied to the resolution note. | Pass / Fail |

---

# 2. Output Format and Parsability

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| F1 | Valid MusicXML | Does the output parse without errors? | Pass / Fail |
| F2 | Correct encoding | Right clefs, key signatures, time signatures, note durations | Count errors |
| F3 | Part assignment | CF and counterpoint correctly placed in the right voices | Pass / Fail |
| F4 | Completeness | All measures present; no truncation or hallucinated extra bars | Pass / Fail |

---

# 3. Prompt Adherence and Consistency

| # | Criterion | Check | Scoring |
|---|-----------|-------|---------|
| P1 | Instruction following | Did the LLM respect the species, the CF, the voice position (above/below)? | Pass / Fail |
| P2 | Consistency across runs | Given the same prompt multiple times, how stable is the quality? | Variance of scores |
| P3 | Self-correction ability | If the LLM explains its reasoning, does the reasoning match the actual output? | Pass / Fail |
| P4 | Hallucination rate | Does the LLM invent rules not in the guide, misstate rules, or claim its output satisfies rules that it violates? | Count instances |
| P5 | Originality of the solution | Does the LLM generate an original solution each time, without reproducing the same or a very similar output across successive generations? | Count instances |

---

# 4. Musical Quality (Expert Assessment)

*Likert scale 1–5, assessed by the evaluator as domain expert.*

| Score | Meaning | Description |
|-------|---------|-------------|
| 1 | Poor | Fundamentally unmusical or incoherent |
| 2 | Weak | Technically passable but clearly flawed |
| 3 | Adequate | What a mediocre student would produce |
| 4 | Good | Competent, musical, minor quibbles only |
| 5 | Excellent | Could appear in a Fux textbook as an example |

## 4A. Melodic Quality of the Counterpoint Line

| # | Criterion | Check |
|---|-----------|-------|
| M1 | Contour and arch | Does the melody have a clear overall shape, a single climax point, placed neither at the very beginning nor at the very end? |
| M2 | Stepwise predominance | Is the line predominantly conjunct (stepwise), with leaps used sparingly for contrast and energy? |
| M3 | Leap quality and placement | Are leaps well chosen (varied interval sizes, not always the same)? Do they occur at musically logical points? |
| M4 | Range utilisation | Does the line explore a reasonable portion of its available range (roughly an octave to a 10th)? |
| M5 | Avoidance of monotony | Does the melody avoid immediate pitch repetition (in species 2–5), mechanical sequential patterns, and aimless oscillation? In 1st species: is pitch repetition used purposefully? |
| M6 | Singability | Could a singer perform this line naturally? No awkward interval successions, no disorienting chains of direction changes? |

## 4B. Contrapuntal Relationship

| # | Criterion | Check |
|---|-----------|-------|
| C1 | Motion variety | Good balance of contrary, oblique, and similar motion |
| C2 | Intervallic variety | Uses a range of consonances (3rds, 6ths, 5ths, 8ths, 10ths), not locked into parallel thirds or sixths |
| C3 | Independence of voices | The counterpoint has its own melodic identity, its own climax, its own rhythm of tension and repose |
| C4 | Tension and release | Moments of tension are balanced by moments of resolution and consonant stability |
| C5 | Cadential convincingness | The cadence feels like a genuine arrival, not just a mechanical landing on the correct interval |
| C6 | Oblique motion quality (1st species) | When pitch repetition is used, does it serve the musical line, or does it feel like the LLM ran out of ideas? |

## 4C. Stylistic Appropriateness

| # | Criterion | Check |
|---|-----------|-------|
| A1 | Modal coherence | The counterpoint sounds like it belongs in the given mode; the character of the mode is audible, not neutralised |
| A2 | Period-appropriate character | Sounds like Renaissance-era pedagogical counterpoint, not Romantic harmony, jazz voice-leading, or modern parallel motion |
| A3 | Pedagogical plausibility | Would this exercise be credible as student work submitted to Fux? Not too simplistic, not suspiciously clever |

## 4D. Scoring

Melodic Quality = average of M1–M6

Contrapuntal Quality = average of C1–C6

Stylistic Quality = average of A1–A3

Overall Musical Quality = (40% × Melodic) + (40% × Contrapuntal) + (20% × Stylistic)

---

# Summary Scorecard

| Category | Sub-category | Metric Type | Contribution |
|----------|-------------|-------------|--------------|
| Rule Compliance | Universal rules (U1–U18) | Violation count (Pass/Fail = 0 or 1; Count = raw total) | Cumulative |
| Rule Compliance | Species-specific rules | Violation count (Pass/Fail = 0 or 1; Count = raw total) | Cumulative |
| Output Format | F1–F4 | Violation count (Pass/Fail = 0 or 1; Count = raw total) | Cumulative |
| Prompt Adherence | P1–P5 | Violation count (Pass/Fail = 0 or 1; Count = raw total) | Cumulative |
| Musical Quality | M1–M6, C1–C6, A1–A3 | Likert 1–5 (manual expert assessment) | Reported separately |

---

# Scoring Methodology

The CAMBIATA assessment framework uses a unified violation-count scoring system in which a lower total indicates a better exercise. Every criterion in Sections 1, 2, and 3 contributes to a single cumulative score calculated as follows.

Pass/Fail criteria are converted to a binary violation score: 0 if the criterion is satisfied, 1 if it is not. Count criteria contribute their raw violation count directly to the total (e.g., three instances of parallel fifths = 3 points). The texture diversity criterion (S5-1) is scored as the number of missing textures: 5 minus the number of distinct textures present (0 if all five are present, 5 if none are).

All violations carry equal weight. No multiplier or weighting coefficient is applied. One parallel fifth counts the same as one failed cadence or one missing texture. This strict equivalence ensures that the total score reflects the raw number of rule infractions without interpretive bias.

Section 4 (Musical Quality) is excluded from the cumulative total. The assessments in Section 4 serve as a manual expert evaluation tool and are reported separately. They are not converted into violation points and do not affect the final score.

The theoretical minimum score is 0, representing a flawless exercise with no violations. There is no fixed maximum; the ceiling depends on the number of applicable criteria for the given species and the length of the exercise.
