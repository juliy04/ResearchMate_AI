import streamlit as st
import fitz  # PyMuPDF
import ollama

# AI function using Ollama and Gemma 3
def ask_gemma(prompt):
    try:
        response = ollama.chat(
            model="gemma3:4b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Error connecting to Ollama: {e}"
# Page configuration
st.set_page_config(
    page_title="ResearchMate AI",
    page_icon="📚",
    layout="wide"
)

# Application title
st.title("📚 ResearchMate AI")
st.subheader("Your AI-Powered Research Assistant")

st.write(
    "Upload academic research papers, extract their text, "
    "and prepare them for summarization and analysis."
)

st.divider()

# Upload a research paper
st.header("📄 Upload Research Paper")

uploaded_file = st.file_uploader(
    "Choose a research paper in PDF format",
    type=["pdf"]
)

if uploaded_file is not None:

    try:
        # Open the uploaded PDF
        pdf_document = fitz.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        )

        # Extract text from all pages
        extracted_text = ""

        for page_number, page in enumerate(pdf_document, start=1):
            extracted_text += (
                f"\n\n--- Page {page_number} ---\n"
                + page.get_text()
            )

        pdf_document.close()

        st.success("Research paper uploaded successfully!")

        # Display document information
        st.write(f"**Number of pages:** {len(extracted_text.split('--- Page ')) - 1}")

        # Display extracted text
        st.header("📖 Extracted Research Paper Text")

        if extracted_text.strip():
            st.text_area(
                "Extracted text",
                value=extracted_text,
                height=350
            )
        else:
            st.warning(
                "No selectable text was found. "
                "This PDF may contain scanned images."
            )

    except Exception as error:
        st.error(f"Unable to read this PDF: {error}")

else:
    st.info("Upload a PDF to begin your research analysis.")

st.divider()

st.caption("ResearchMate AI | Academic Research Assistant")
# Research Paper Summarizer

st.divider()
st.header("📝 Research Paper Summarizer")

if uploaded_file is not None and extracted_text.strip():

    if st.button("Generate Research Summary"):

        text = extracted_text
        text_lower = text.lower()

        st.subheader("🎯 Research Objective")

        objective_keywords = [
            "objective", "aim", "purpose", "this study",
            "this research", "we propose"
        ]

        objective_found = False

        for keyword in objective_keywords:
            position = text_lower.find(keyword)

            if position != -1:
                st.write(
                    text[max(0, position - 100):position + 500]
                )
                objective_found = True
                break

        if not objective_found:
            st.write(
                "No obvious objective section was found. "
                "Please review the paper's introduction."
            )

        st.subheader("🔬 Research Methodology")

        methodology_keywords = [
            "methodology", "method", "approach",
            "experimental setup", "proposed model"
        ]

        methodology_found = False

        for keyword in methodology_keywords:
            position = text_lower.find(keyword)

            if position != -1:
                st.write(
                    text[max(0, position - 100):position + 500]
                )
                methodology_found = True
                break

        if not methodology_found:
            st.write(
                "No obvious methodology section was found."
            )

        st.subheader("📊 Key Findings")

        findings_keywords = [
            "results", "findings", "our results",
            "experimental results", "performance"
        ]

        findings_found = False

        for keyword in findings_keywords:
            position = text_lower.find(keyword)

            if position != -1:
                st.write(
                    text[max(0, position - 100):position + 500]
                )
                findings_found = True
                break

        if not findings_found:
            st.write(
                "No obvious findings section was found."
            )

        st.subheader("✅ Conclusion")

        conclusion_keywords = [
            "conclusion", "in conclusion",
            "we conclude", "future work"
        ]

        conclusion_found = False

        for keyword in conclusion_keywords:
            position = text_lower.find(keyword)

            if position != -1:
                st.write(
                    text[max(0, position - 100):position + 500]
                )
                conclusion_found = True
                break

        if not conclusion_found:
            st.write(
                "No obvious conclusion section was found."
            )

else:
    st.info(
        "Upload a research paper PDF above before generating a summary."
    )
# AI-Powered Research Paper Summarizer
st.divider()
st.header("🤖 AI Research Paper Summarizer")

if uploaded_file is not None and extracted_text.strip():
    if st.button("Generate AI Summary"):
        with st.spinner("Gemma 3 is analyzing your research paper..."):
            prompt = f"""
You are a research assistant. Analyze the research paper below.

Write a clear summary using these sections:
1. Research Objective
2. Methodology
3. Key Findings
4. Conclusion

Use simple English. Do not invent information that is
not supported by the paper.

Research paper text:
{extracted_text[:12000]}
"""
            summary = ask_gemma(prompt)
            st.markdown(summary)
else:
    st.info("Please upload a research paper PDF first.")   
    # Ask the Paper
st.divider()
st.header("💬 Ask the Paper")

if uploaded_file is not None and extracted_text.strip():

    question = st.text_input(
        "Ask a question about your uploaded research paper:",
        placeholder="Example: What is the main objective of this research?"
    )

    if st.button("Find Answer"):

        if not question.strip():
            st.warning("Please enter a question first.")

        else:
            # Split the extracted paper into sentences
            import re

            sentences = re.split(
                r'(?<=[.!?])\s+',
                extracted_text
            )

            # Find words that may be useful for matching
            stop_words = {
                "what", "which", "when", "where", "who",
                "why", "how", "does", "did", "the",
                "is", "are", "was", "were", "a",
                "an", "and", "or", "of", "in", "to",
                "for", "on", "with", "this", "that",
                "their", "they", "it", "about", "paper"
            }

            question_words = {
                word.lower()
                for word in re.findall(r'\b[a-zA-Z]+\b', question)
                if word.lower() not in stop_words
            }

            # Score each sentence by matching question words
            scored_sentences = []

            for sentence in sentences:
                sentence_words = {
                    word.lower()
                    for word in re.findall(
                        r'\b[a-zA-Z]+\b',
                        sentence
                    )
                }

                score = len(question_words & sentence_words)

                if score > 0:
                    scored_sentences.append((score, sentence.strip()))

            # Show the most relevant matching sentences
            scored_sentences.sort(
                key=lambda item: item[0],
                reverse=True
            )

            best_sentences = []
            seen_sentences = set()

            for score, sentence in scored_sentences:
                if sentence and sentence not in seen_sentences:
                    best_sentences.append(sentence)
                    seen_sentences.add(sentence)

                if len(best_sentences) == 3:
                    break

            if best_sentences:
                st.subheader("📖 Relevant Information")
                st.write(" ".join(best_sentences))
                st.caption(
                    "This answer is based on keyword matching. "
                    "Verify it against the original research paper."
                )
            else:
                st.warning(
                    "No relevant sentences were found. "
                    "Try using keywords from the paper."
                )

else:
    st.info("Upload a research paper PDF before asking questions.")
    # Compare Research Papers
st.divider()
st.header("📚 Compare Two Research Papers")

st.write(
    "Upload two research papers to compare their objectives, "
    "methodologies, findings, and conclusions."
)

paper1_file = st.file_uploader(
    "Upload Research Paper 1",
    type=["pdf"],
    key="comparison_paper1"
)

paper2_file = st.file_uploader(
    "Upload Research Paper 2",
    type=["pdf"],
    key="comparison_paper2"
)


def extract_pdf_text(pdf_file):
    """Extract text from an uploaded PDF."""
    if pdf_file is None:
        return ""

    try:
        with fitz.open(
            stream=pdf_file.getvalue(),
            filetype="pdf"
        ) as document:
            return "\n".join(
                page.get_text()
                for page in document
            )
    except Exception:
        return ""


if st.button("Compare Papers"):

    if paper1_file is None or paper2_file is None:
        st.warning("Please upload both research papers.")

    else:
        paper1_text = extract_pdf_text(paper1_file)
        paper2_text = extract_pdf_text(paper2_file)

        if not paper1_text.strip() or not paper2_text.strip():
            st.error(
                "Unable to extract text from one or both PDFs. "
                "Please check that the files contain selectable text."
            )

        else:
            import re

            def find_section(text, keywords):
                """Find a short passage near a matching keyword."""
                text_lower = text.lower()

                for keyword in keywords:
                    position = text_lower.find(keyword)

                    if position != -1:
                        return text[
                            max(0, position - 80):
                            position + 400
                        ].strip()

                return "No matching section found."

            sections = {
                "Research Objective": [
                    "objective", "aim", "purpose"
                ],
                "Methodology": [
                    "methodology", "method", "approach"
                ],
                "Key Findings": [
                    "results", "findings", "experimental results"
                ],
                "Conclusion": [
                    "conclusion", "in conclusion"
                ]
            }

            st.subheader("📊 Comparison Results")

            for section_name, keywords in sections.items():

                with st.expander(section_name, expanded=True):

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Research Paper 1**")
                        st.write(
                            find_section(paper1_text, keywords)
                        )

                    with col2:
                        st.markdown("**Research Paper 2**")
                        st.write(
                            find_section(paper2_text, keywords)
                        )

            st.success("Paper comparison completed.")

            st.caption(
                "This prototype locates text using keywords. "
                "It does not independently determine whether "
                "the papers agree or disagree."
            )

st.divider()
# Research Notes Generator
st.divider()
st.header("📝 Research Notes Generator")

st.write(
    "Generate organized study notes from your uploaded research paper."
)

if uploaded_file is not None and extracted_text.strip():

    if st.button("Generate Research Notes"):

        notes_text = extracted_text
        notes_lower = notes_text.lower()

        def extract_note_section(text, keywords, max_length=700):
            """Find text near a relevant research section."""
            text_lower = text.lower()

            for keyword in keywords:
                position = text_lower.find(keyword)

                if position != -1:
                    start = max(0, position - 100)
                    end = min(len(text), position + max_length)

                    return text[start:end].strip()

            return "No matching section was found in the document."

        # Extract notes for different research sections
        objective = extract_note_section(
            notes_text,
            ["objective", "aim", "purpose", "research question"]
        )

        methodology = extract_note_section(
            notes_text,
            ["methodology", "methods", "approach", "experimental setup"]
        )

        findings = extract_note_section(
            notes_text,
            ["results", "findings", "experimental results"]
        )

        conclusion = extract_note_section(
            notes_text,
            ["conclusion", "in conclusion", "future work"]
        )

        # Display the research notes
        st.subheader("📚 Your Research Notes")

        st.markdown("### 1. Research Topic")
        st.write("Based on the uploaded research paper.")

        st.markdown("### 2. Research Objectives")
        st.write(objective)

        st.markdown("### 3. Methodology")
        st.write(methodology)

        st.markdown("### 4. Key Findings")
        st.write(findings)

        st.markdown("### 5. Conclusion")
        st.write(conclusion)

        # Prepare notes for download
        notes_for_download = f"""
RESEARCHMATE AI - RESEARCH NOTES

RESEARCH TOPIC
Based on the uploaded research paper.

RESEARCH OBJECTIVES
{objective}

METHODOLOGY
{methodology}

KEY FINDINGS
{findings}

CONCLUSION
{conclusion}
"""

        st.download_button(
            label="📥 Download Research Notes",
            data=notes_for_download,
            file_name="research_notes.txt",
            mime="text/plain"
        )

else:
    st.info(
        "Upload a research paper in the PDF section above "
        "before generating notes."
    )