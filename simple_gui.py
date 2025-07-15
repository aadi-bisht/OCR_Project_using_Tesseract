import pandas as pd
import streamlit as st
import process_file


def main():
    processed = False
    st.title("[OCR] Business Name Validator")
    uploaded_file = st.file_uploader(
        "Choose a CSV file (encoding UTF-8)"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("CSV file uploaded successfully!")
            processed = process_file.process_file(df, st)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

    if processed:
        st.success("Character recognition was performed successfully!")
        st.write("Here is a preview of the processed data:")
        st.dataframe(df.head())
        csv = df.to_csv(index=False)
        st.download_button(label="Download Processed Data", data=csv, file_name="processed_data.csv", mime='text/csv')


if __name__ == '__main__':
    main()