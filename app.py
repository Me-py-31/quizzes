import os
import pandas as pd
import streamlit as st
from docx import Document

st.set_page_config(
    page_title="Question Bank Collector", page_icon="📝", layout="centered"
)

st.title("📝 Question Bank Data Collector")
st.write("Enter your table details and questions below to export to Excel or Word.")

# Form to collect Table Number and Number of Questions
with st.form("question_entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        table_number = st.text_input("Table Number / Identifier", value="1")
    with col2:
        num_questions = st.number_input(
            "Number of Questions to Memorize",
            min_value=1,
            max_value=50,
            value=3,
            step=1,
        )

    st.markdown("---")
    st.subheader("Enter Questions")

    # Dynamic input box generation
    questions_data = []
    for i in range(int(num_questions)):
        st.markdown(f"**Item #{i+1}**")
        q_col1, q_col2 = st.columns([1, 3])
        with q_col1:
            q_num = st.text_input(
                "Question Number", value=f"Q{i+1}", key=f"q_num_{i}"
            )
        with q_col2:
            q_text = st.text_area(
                "Question Text",
                placeholder="Type the question content here...",
                key=f"q_text_{i}",
                height=70,
            )

        questions_data.append(
            {
                "Table Number": table_number,
                "Question Number": q_num,
                "Question": q_text,
            }
        )

    st.markdown("---")
    export_format = st.radio(
        "Select Export Format:", ["Excel (.xlsx)", "Word Document (.docx)", "CSV"]
    )
    submit_btn = st.form_submit_button("Generate & Download Document")

if submit_btn:
    df = pd.DataFrame(questions_data)

    if export_format == "Excel (.xlsx)":
        filename = f"Table_{table_number}_Questions.xlsx"
        df.to_excel(filename, index=False)
        with open(filename, "rb") as f:
            st.download_button("📥 Download Excel Spreadsheet", f, file_name=filename)
        st.success(f"Successfully generated {filename}!")

    elif export_format == "Word Document (.docx)":
        filename = f"Table_{table_number}_Questions.docx"
        doc = Document()
        doc.add_heading(f"Table {table_number} - Question Bank", level=1)

        # Add structured table
        table = doc.add_table(rows=1, cols=3)
        table.style = "Table Grid"
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Table Number"
        hdr_cells[1].text = "Question Number"
        hdr_cells[2].text = "Question Text"

        for entry in questions_data:
            row_cells = table.add_row().cells
            row_cells[0].text = str(entry["Table Number"])
            row_cells[1].text = str(entry["Question Number"])
            row_cells[2].text = str(entry["Question"])

        doc.save(filename)
        with open(filename, "rb") as f:
            st.download_button("📥 Download Word Document", f, file_name=filename)
        st.success(f"Successfully generated {filename}!")

    elif export_format == "CSV":
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download CSV File",
            csv_bytes,
            file_name=f"Table_{table_number}_Questions.csv",
            mime="text/csv",
        )
        st.success("CSV generated successfully!")