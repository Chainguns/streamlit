import streamlit as st
import pandas as pd
import polars as pl
import time

st.title("Comparing Pandas and PyPolars Dataframes")

st.header("Introduction")
st.write("Pandas is a popular data analysis library in Python, while PyPolars is a relatively new library, "
         "that aims to provide faster data processing capabilities.")

st.header("Loading the Iris Dataset")

iris = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
iris_polars = pl.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")

st.write("Pandas DataFrame Shape:", iris.shape)
st.write("PyPolars DataFrame Shape:", iris_polars.shape)

st.header("DataFrame Operations")
st.write("We will perform some common dataframe operations on both Pandas and PyPolars dataframes")

st.write("Pandas head:")
st.write(iris.head())
st.write("PyPolars head:")
st.write(iris_polars.head())

st.write("Pandas describe:")
st.write(iris.describe())
st.write("PyPolars describe:")
st.write(iris_polars.describe())

st.header("Groupby Operations")
st.write("We will perform a groupby operation on both Pandas and PyPolars dataframes")

st.write("Pandas groupby mean:")
st.write(iris.groupby("species").mean())
st.write("PyPolars groupby mean:")
st.write(iris_polars.groupby("species").mean())

st.header("Apply Operations")
st.write("We will perform an apply operation on both Pandas and PyPolars dataframes")

def custom_operation(row):
    return row["sepal_length"] / row["sepal_width"]

st.write("Pandas apply result:")
st.write(iris.apply(custom_operation, axis=1))
st.write("PyPolars apply result:")
st.write(iris_polars.apply(custom_operation, axis=1))

st.header("Performance Comparison")
st.write("We will compare the performance of Pandas and PyPolars dataframes")

start = time.time()
iris.groupby("species").mean()
end = time.time()
pandas_time = end - start

start = time.time()
iris_polars.groupby("species").mean()
end = time.time()
polars_time = end - start

st.write("Pandas groupby time:", pandas_time)
st.write("PyPolars groupby time:", polars_time)
