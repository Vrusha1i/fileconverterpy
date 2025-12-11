import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

def main():
    st.title("File Converter - Excel/CSV to CSV")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])
    
    if uploaded_file is not None:
        # Read the file
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            st.success(f"File loaded successfully! Shape: {df.shape}")
            
            # Replace empty cells with 'Null'
            df = df.fillna('Null')
            df = df.replace('', 'Null')
            
            # Show original data preview
            st.subheader("Original Data Preview")
            st.dataframe(df.head())
            
            # Column mapping section
            st.subheader("Column Mapping")
            
            # Get target columns from the sample file
            target_columns = [
                'Name', 'Application Ref. No.', 'Application Status', 'Stage', 
                'Program Name', 'Selected Card Variant', 'Location Name', 
                'Phone Number', 'Utm Campaign', 'Utm Medium', 'owner', 
                'what to do', 'calling prioerty', 'Created Date', 'Journey Type', 
                'Soft Decision', 'Sub Stage'
            ]
            
            # Create column mapping
            column_mapping = {}
            source_columns = ['None'] + list(df.columns)
            
            for target_col in target_columns:
                selected_col = st.selectbox(
                    f"Map '{target_col}' to:",
                    source_columns,
                    key=f"map_{target_col}"
                )
                if selected_col != 'None':
                    column_mapping[target_col] = selected_col
            
            # Program Name selection
            st.subheader("Program Name Configuration")
            program_option = st.selectbox("Select Program Name:", ["IDFC", "BOB"])
            
            # Convert button
            if st.button("Convert to CSV"):
                # Create new dataframe with target structure
                new_df = pd.DataFrame()
                
                # Map columns
                for target_col, source_col in column_mapping.items():
                    if source_col in df.columns:
                        new_df[target_col] = df[source_col]
                    else:
                        new_df[target_col] = 'Null'
                
                # Add unmapped target columns with 'Null'
                for target_col in target_columns:
                    if target_col not in new_df.columns:
                        new_df[target_col] = 'Null'
                
                # Set Program Name
                new_df['Program Name'] = program_option
                
                # Reorder columns to match target format
                new_df = new_df[target_columns]
                
                # Show converted data preview
                st.subheader("Converted Data Preview")
                st.dataframe(new_df.head())
                
                # Download button
                csv_buffer = BytesIO()
                new_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                st.download_button(
                    label="Download Converted CSV",
                    data=csv_buffer.getvalue(),
                    file_name="converted_file.csv",
                    mime="text/csv"
                )
                
                st.success("File converted successfully!")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    main()