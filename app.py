import streamlit as st
from utils import searcher
import pandas as pd

examples = pd.read_csv("samples.csv",delimiter=";")

st.title('Missing letter solver based on WordNet')

col1, col2 = st.columns(2)

with col1:

    form = st.form(key='my-form')
    masked = form.text_input('Enter masked word', 't--t')
    defin = form.text_input('Enter definition', 'the words of something written')
    sim_thr = form.slider(label='Select threshold', value=0.8, min_value=0.00, max_value=1.00, key=4)
    submit = form.form_submit_button('Submit')

    if submit:
        st.subheader("Possible words in context to the given definition:")
        response = searcher(masked,defin,sim_thr)

        if len(response) >0:
            for i in response:
                st.markdown("- " + i)
        else:
            st.markdown("No words found in dictionary")

with col2:
    st.caption('Some examples to try')
    st.dataframe(examples)
