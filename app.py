import streamlit as st
import numpy as py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))

if web_apps == "Exploratory Data Analysis":
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)

        # Display relevant statistics about the dataset
        st.write("Number of Rows:", len(df))
        st.write("Number of Columns:", len(df.columns))
        st.write("Number of Categorical Variables:",
                 len(df.select_dtypes(include=['object'])))
        st.write("Number of Numerical Variables:",
                 len(df.select_dtypes(include=['int64', 'float64'])))
        st.write("Number of Boolean Variables:",
                 len(df.select_dtypes(include=['bool'])))

        show_df = st.checkbox("Show Data Frame")

        if show_df:
            st.write(df)

        column_type = st.sidebar.selectbox('Select Data Type',
                                           ("Numerical", "Categorical"))

        if column_type == "Numerical":
            numerical_column = st.sidebar.selectbox(
                'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

            # Five number summary
            summary = df[numerical_column].describe()
            st.write("Five Number Summary:")
            st.write(summary)

            # Histogram
            choose_color = st.color_picker('Pick a Color', "#69b3a2")
            choose_opacity = st.slider(
                'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)
            hist_bins = st.slider('Number of bins', min_value=5,
                                  max_value=150, value=30)
            hist_title = st.text_input('Set Title', 'Histogram')
            hist_xtitle = st.text_input(
                'Set x-axis Title', numerical_column)

            fig, ax = plt.subplots()
            ax.hist(df[numerical_column], bins=hist_bins,
                    edgecolor="black", color=choose_color, alpha=choose_opacity)
            ax.set_title(hist_title)
            ax.set_xlabel(hist_xtitle)
            ax.set_ylabel('Count')

            st.pyplot(fig)

        elif column_type == "Categorical":
            categorical_column = st.sidebar.selectbox(
                'Select a Column', df.select_dtypes(include=['object']).columns)

            # Proportions of each category level
            category_counts = df[categorical_column].value_counts()
            category_proportions = category_counts / len(df)
            st.write("Category Proportions:")
            st.write(category_proportions)

            # Bar plot
            plt.figure()
            sns.countplot(data=df, x=categorical_column)
            plt.xticks(rotation=90)
            st.pyplot()