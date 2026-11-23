# Review of 15 difficult benchmark queries

Five held-out cases per language, with distinct base intents. Cases are selected for retrieval misses, false refusals and missing information.

## English

### Q003_english

How long is the usual window to request a marks review after results?

- Expected answer: 15 days.
- Expected evidence: DOC01_P002. Top result: DOC01_P021, Section 23 — Make-up exams.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: The typical window for requesting a marks review after results can vary depending on several factors such as the specific institution or program, and may be up to 1-2 months in some cases. It's important to check with the relevant department or office of the institution
- RAG output: UNANSWERABLE

### Q004_english

How do I formally request a recheck of my marks?

- Expected answer: Submit the prescribed form and fee to the Controller of Examinations.
- Expected evidence: DOC01_P002. Top result: DOC01_P004, Section 20 / Results.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: To formally request a recheck of your marks, follow these steps:  1. **Review Your Exam**: Ensure that all parts of the exam were completed correctly and accurately.  2. **Check for Errors**: Look for any errors or mistakes in your answers, such
- RAG output: UNANSWERABLE

### Q012_english

How can I pay the re-evaluation charge in instalments?

- Expected answer: UNANSWERABLE.
- Expected evidence: none. Top result: DOC01_P002, Section 20 / Applying.
- Observation: The score gate accepted a topical match whose passage does not contain the requested detail.
- DIRECT output: To pay the re-evaluation charge in installments, follow these steps:  1. **Review Your Account Details**: Ensure that your account details (such as credit card number, expiration date, and CVV code) match those provided on your invoice.  2.
- RAG output: UNANSWERABLE

### Q005_english

What size of change in marks triggers a second independent re-check?

- Expected answer: More than 20%.
- Expected evidence: DOC01_P003. Top result: DOC01_P003, Section 20 / Examiner.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: The size of the change in marks that triggers a second independent re-check is typically 10% or more. This means that if there's a significant change in the mark, such as an increase or decrease from the previous year, it would trigger a second
- RAG output: UNANSWERABLE

### Q041_english

Please specify the person asked to verify an allegedly out-of-syllabus question.

- Expected answer: Course coordinator.
- Expected evidence: DOC01_P018. Top result: DOC01_P018, Sections 7.3 and 19 — Exam grievances.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: The person who is supposed to verify an allegedly out-of-syllabus question is typically the instructor or teacher of that course or subject matter.
- RAG output: UNANSWERABLE

## Hindi

### Q006_hindi

संशोधित अंकपत्र लेने से पहले पुराने अंकपत्र का क्या करना होगा?

- Expected answer: Surrender the previous grade sheet.
- Expected evidence: DOC01_P004. Top result: DOC01_P002, Section 20 / Applying.
- Observation: The expected passage was absent from the top five. A generator limited to those passages cannot cite it.
- DIRECT output: संशोधित अंकपत्र लेने से पहले पुराने अंकपत्र का करना जैसी द
- RAG output: UNANSWERABLE

### Q001_hindi

क्या मेकअप की थ्योरी परीक्षा की कॉपी दोबारा जँच सकती है?

- Expected answer: Yes.
- Expected evidence: DOC01_P001. Top result: DOC01_P001, Section 20 / Eligibility.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: उसके अनुवादित विश्लेषण में, मेकअप की थ्योरी परीक्षा की कॉ
- RAG output: UNANSWERABLE

### Q115_hindi

कृपया बताएँ: परीक्षा कक्ष के बाहर फ़ोन रखने की लॉकर जमा राशि क्या है?

- Expected answer: UNANSWERABLE.
- Expected evidence: none. Top result: DOC01_P033, Sections 30 and 32 — Progression and withdrawal.
- Observation: The score gate accepted a topical match whose passage does not contain the requested detail.
- DIRECT output: कुछ महत्वपूर्ण अंग्रेजी सबसे आधिकारिक दर्शन:  1. निम्नलि�
- RAG output: Grade for compulsory medical semester withdrawal: W.

### Q008_hindi

अगर मैं कई प्रवेश छात्रवृत्तियों के लिए पात्र हूँ, तो मुझे कौन-सी मिलेगी?

- Expected answer: The highest-value scholarship.
- Expected evidence: DOC02_P006. Top result: DOC01_P027, Section 24 — Supplementary exams.
- Observation: The expected passage was absent from the top five. A generator limited to those passages cannot cite it.
- DIRECT output: मुझे कौन-सी मिलेगी। मैं अपने पात्रों का सबसे बड़ा व्यक्त
- RAG output: UNANSWERABLE

### Q007_hindi

परिणाम प्रकाशित होने के कितने समय बाद ट्रांसक्रिप्ट जारी होती है?

- Expected answer: After 15 days.
- Expected evidence: DOC01_P005. Top result: DOC03_P009, Results / Odd semester AY 2024–25.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: ट्रांसक्रिप्ट जारी होती है 10-20 महीनेस्ट।
- RAG output: UNANSWERABLE

## Hinglish

### Q019_hinglish

har scheduled class ki attendance unit bata sakte ho?

- Expected answer: One unit.
- Expected evidence: DOC01_P010. Top result: DOC01_P010, Section 10 — Attendance.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: UNANSWERABLE
- RAG output: UNANSWERABLE

### Q022_hinglish

university represent karne par attendance relief ke liye prior approval bata sakte ho?

- Expected answer: Prior approval of the Dean.
- Expected evidence: DOC01_P011. Top result: DOC01_P012, Section 10 — Attendance.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: The university must obtain prior approval from the Ministry of Education before implementing attendance reduction measures.
- RAG output: UNANSWERABLE

### Q107_hinglish

exam grievance email ki maximum word limit bata do.

- Expected answer: UNANSWERABLE.
- Expected evidence: none. Top result: DOC01_P017, Sections 7.3 and 19 — Exam grievances.
- Observation: The score gate accepted a topical match whose passage does not contain the requested detail.
- DIRECT output: The maximum word limit for an exam grievance email is typically 100 words. This limit ensures that emails are concise and to the point while still providing enough information for the recipient to understand the issue clearly.
- RAG output: The maximum word limit for emails related to examination grievances is 240 characters.

### Q034_hinglish

faculty marks enter karne wala portal bata sakte ho?

- Expected answer: ERP.
- Expected evidence: DOC01_P016. Top result: DOC01_P016, Sections 17–18 — Result approval.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: To determine if faculty marks can be entered into Karne Wala Portal:  1. First, identify the correct portal: Karne Wala Portal is not a standard portal name or location.  2. Next, consider the context of the question: The question asks
- RAG output: UNANSWERABLE

### Q035_hinglish

grade report generate hone ka stage bata do.

- Expected answer: After grades are locked in the ERP.
- Expected evidence: DOC01_P016. Top result: DOC01_P016, Sections 17–18 — Result approval.
- Observation: The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation.
- DIRECT output: Grade Report Generate Hone Kā Stage Bata Do  Grade Report Generate Hone Kā Stage Bata Do is a process in which a teacher or educational institution creates a detailed report of a student's performance and progress over time. This type of report typically
- RAG output: UNANSWERABLE
