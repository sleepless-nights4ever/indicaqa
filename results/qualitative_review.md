# Qualitative review of 16 held-out queries

Ranks and refusals use the saved pilot predictions. Refusal here means the confidence gate decision before generation.

## Q001_hindi
क्या मेकअप की थ्योरी परीक्षा की कॉपी दोबारा जँच सकती है?

Devanagari vocabulary for a make-up theory paper shares little surface text with English. Keep the theory-paper restriction when generating.

- BM25 · gold rank 1 · score gate refused · top passage DOC01_P001
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P001

## Q001_hinglish
Makeup theory paper ki rechecking ho sakti hai?

Roman-script rechecking co-occurs with English theory paper. Retrieving a generic review passage would omit eligibility.

- BM25 · gold rank 1 · score gate refused · top passage DOC01_P001
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P001

## Q002_english
Does the rechecking option also cover a supplementary exam?

Supplementary exams are excluded. A match on “exam” alone can return make-up eligibility and flip the answer.

- BM25 · gold rank 1 · score gate refused · top passage DOC01_P001
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P001

## Q002_hinglish
Supple exam ka paper bhi recheck karwa sakte hain?

The abbreviation “supple” can obscure the difference between supplementary and make-up exams.

- BM25 · gold rank 2 · score gate refused · top passage DOC01_P005
- Hybrid · gold rank 3 · score gate passed · top passage DOC01_P005

## Q003_hindi
नतीजे आने के बाद नंबर दोबारा जँचवाने के लिए आम तौर पर कितने दिन मिलते हैं?

The answer is a duration from announcement. A transcript passage also mentions 15 days, so numeric agreement alone does not establish grounding.

- BM25 · gold rank 2 · score gate refused · top passage DOC01_P001
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P002

## Q003_hinglish
Result aane ke baad marks recheck ke liye normally kitne din milte hain?

The words result, marks, and recheck can point to several stages. The expected evidence concerns applying for review.

- BM25 · gold rank 2 · score gate refused · top passage DOC01_P005
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P002

## Q005_english
What size of change in marks triggers a second independent re-check?

The cutoff is strictly over 20%. Preserve the inequality and the trigger for a second evaluator.

- BM25 · gold rank 2 · score gate refused · top passage DOC01_P004
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P003

## Q005_hinglish
Marks kitne change ho jaaye toh ek aur evaluator ko copy jaati hai?

Code mixing retains “evaluator” but does not quote the numeric cutoff. The selected passage needs to explain when the second evaluator is required.

- BM25 · gold rank 1 · score gate refused · top passage DOC01_P003
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P003

## Q006_english
What must I do with my old marksheet before I can receive a revised one?

Marksheet and grade sheet refer to the same record. The required action is surrender of the old sheet.

- BM25 · gold rank 1 · score gate refused · top passage DOC01_P004
- Hybrid · gold rank 1 · score gate passed · top passage DOC01_P004

## Q007_hindi
परिणाम प्रकाशित होने के कितने समय बाद ट्रांसक्रिप्ट जारी होती है?

The borrowed word for transcript appears in Devanagari. The re-evaluation deadline is a nearby distractor with the same number.

- BM25 · gold rank 5 · score gate refused · top passage DOC01_P001
- Hybrid · gold rank 3 · score gate passed · top passage DOC03_P009

## Q009_hinglish
Admission pe scholarship nahi mili thi, toh academic wali kitne percent ki mil sakti hai?

The 10% academic award differs from continuing an existing award. The question carries the entry-without-award qualifier.

- BM25 · gold rank 1 · score gate passed · top passage DOC02_P007
- Hybrid · gold rank 1 · score gate passed · top passage DOC02_P007

## Q010_english
When did the notice say the May 2025 exams for CSE semester 2 would be declared?

Check named programme, semester and year together. The notice date and the stated CSE result date differ.

- BM25 · gold rank 1 · score gate passed · top passage DOC03_P008
- Hybrid · gold rank 1 · score gate passed · top passage DOC03_P008

## Q011_hinglish
AY 2024-25 odd sem supple ka result kis date pe announce hua?

“Odd sem supple” identifies a separate result from odd semester make-up. Mixing those events changes the date.

- BM25 · gold rank 1 · score gate refused · top passage DOC03_P009
- Hybrid · gold rank 1 · score gate passed · top passage DOC03_P009

## Q012_english
How can I pay the re-evaluation charge in instalments?

Fee language can match the source even though instalment instructions are absent. Retrieval scores alone measure topical match.

- BM25 · gold rank no gold evidence · score gate passed · top passage DOC01_P002
- Hybrid · gold rank no gold evidence · score gate passed · top passage DOC01_P002

## Q014_hinglish
May 2025 exam admit card pe galat photo fix karwane ki last date kya thi?

The month and examination could lead to the results notice. That notice does not provide a hall-ticket correction deadline.

- BM25 · gold rank no gold evidence · score gate passed · top passage DOC03_P008
- Hybrid · gold rank no gold evidence · score gate passed · top passage DOC03_P008

## Q016_hindi
प्रवेश पोर्टल पर छात्रवृत्ति का प्रमाण अपलोड करने की अधिकतम फ़ाइल सीमा क्या है?

Scholarship and admissions are in scope. The upload-size limit is absent from the pilot, so a topical match is insufficient.

- BM25 · gold rank no gold evidence · score gate refused · top passage DOC01_P001
- Hybrid · gold rank no gold evidence · score gate passed · top passage DOC02_P007
