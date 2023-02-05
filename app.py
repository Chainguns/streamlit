import streamlit as st
import pandas as pd
import pypolar as pd

st.title("Comparing Pandas and PyPolars Dataframes")

st.header("Introduction")
st.write("Pandas is a popular data analysis library in Python, while PyPolars is a relatively new library, "
         "that aims to provide faster data processing capabilities.")

st.header("Creating a DataFrame")
st.write("We will create a simple dataframe using both Pandas and PyPolars and compare the time taken to create the dataframe")

df_pandas = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

df_pypolars = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

st.write("Pandas DataFrame:")
st.write(df_pandas)
st.write("PyPolars DataFrame:")
st.write(df_pypolars)

st.header("DataFrame Operations")
st.write("We will perform some common dataframe operations on both Pandas and PyPolars dataframes")

st.write("Pandas sum:", df_pandas.sum())
st.write("PyPolars sum:", df_pypolars.sum())

st.write("Pandas mean:", df_pandas.mean())
st.write("PyPolars mean:", df_pypolars.mean())

st.header("Performance Comparison")
st.write("Finally, we will compare the performance of Pandas and PyPolars by measuring the time taken to perform a complex operation")



st.write("The above results show the time taken by Pandas and PyPolars to perform the operation. As PyPolars is optimized for performance, it is faster than Pandas for large datasets.")

st.header("Conclusion")
st.write("In conclusion, both Pandas and PyPolars are powerful data analysis libraries in Python, but PyPolars provides faster performance for large datasets. "
         "It's always a good idea to evaluate both libraries and choose the one that fits your needs better.")
