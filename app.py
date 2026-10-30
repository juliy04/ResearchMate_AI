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
# ===== RESEARCHMATE AI — PREMIUM LUXURY THEME =====

st.markdown("""
<style>

/* Premium typography */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

/* Main application background */
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%,
        rgba(198, 164, 98, 0.10), transparent 36%),
        radial-gradient(ellipse at 95% 20%,
        rgba(48, 153, 143, 0.08), transparent 32%),
        #0B0D12;
    color: #EDE9E0;
    font-family: 'DM Sans', sans-serif;
}

/* Main content spacing */
.block-container {
    max-width: 1250px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* Premium headings */
h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.7px;
}

h1 {
    color: #F3E8D0 !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
}

h2 {
    color: #E8D6B0 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

h3 {
    color: #C9A96E !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
}

/* Body text */
p, label, .stMarkdown, li {
    font-family: 'DM Sans', sans-serif;
    color: #C5C5C9;
    line-height: 1.75;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14161D, #0B0D12);
    border-right: 1px solid #302A20;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #D8BA7B !important;
}

/* Gold premium buttons */
.stButton > button {
    background: linear-gradient(135deg, #E5CD98, #B99250);
    color: #17140E !important;
    border: 1px solid #E5CD98;
    border-radius: 10px;
    min-height: 45px;
    padding: 0.6rem 1.25rem;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #F4E3B9, #D2AD69);
    border-color: #F4E3B9;
    box-shadow: 0 0 22px rgba(212, 175, 104, 0.22);
    transform: translateY(-2px);
}

/* File upload panel */
[data-testid="stFileUploader"] {
    background: rgba(24, 26, 33, 0.85);
    border: 1px solid #383126;
    border-radius: 16px;
    padding: 1rem;
}

[data-testid="stFileUploader"] section {
    background: #11141B;
    border: 1px dashed #8C754A;
    border-radius: 12px;
}

[data-testid="stFileUploader"] button {
    color: #E1C58D !important;
    border-color: #A88B57 !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background: #141720 !important;
    color: #F0EBDD !important;
    border: 1px solid #393A40 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #C9A96E !important;
    box-shadow: 0 0 0 1px #C9A96E !important;
}

/* Dropdowns */
[data-testid="stSelectbox"] > div > div {
    background: #171922;
    border-color: #393A40;
    border-radius: 10px;
    color: #EDE9E0;
}

/* Expandable panels */
[data-testid="stExpander"] {
    background: rgba(22, 24, 31, 0.9);
    border: 1px solid #373127;
    border-radius: 13px;
}

/* Notification panels */
[data-testid="stAlert"] {
    background: #171922;
    border: 1px solid #39352C;
    border-radius: 12px;
}

/* Elegant separators */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #8F7549,
        #C9A96E,
        transparent
    );
    margin: 2rem 0;
}

/* Download buttons */
.stDownloadButton > button {
    background: #171922;
    color: #D9BD82 !important;
    border: 1px solid #9B7C46;
    border-radius: 10px;
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stDownloadButton > button:hover {
    background: #25231E;
    border-color: #D9BD82;
    box-shadow: 0 0 16px rgba(201, 169, 110, 0.15);
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #373127;
    border-radius: 12px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0B0D12;
}

::-webkit-scrollbar-thumb {
    background: #5C4B32;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #C9A96E;
}

/* Hide default Streamlit footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

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