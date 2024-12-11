import streamlit as st
import pandas as pd
import altair as alt

# Callback function for clearing values
def clear_values():
    for key in ['planned_production', 'actual_run_time', 'target_part_count', 
                'total_parts_made', 'good_parts']:
        if key in st.session_state:
            del st.session_state[key]

# Initialize session state
if 'planned_production' not in st.session_state:
    st.session_state.planned_production = 0.0
if 'actual_run_time' not in st.session_state:
    st.session_state.actual_run_time = 0.0
if 'target_part_count' not in st.session_state:
    st.session_state.target_part_count = 0.0
if 'total_parts_made' not in st.session_state:
    st.session_state.total_parts_made = 0.0
if 'good_parts' not in st.session_state:
    st.session_state.good_parts = 0.0

st.title('OEE Calculator')

# Clear Values button (move it to the top)
if st.button('Clear Values', on_click=clear_values):
    st.rerun()

# Input fields with session state
planned_production = st.number_input('Planned production time', min_value=0.0, value=st.session_state.planned_production, format="%.1f", key='planned_production')
actual_run_time = st.number_input('Actual Run Time', min_value=0.0, value=st.session_state.actual_run_time, format="%.1f", key='actual_run_time')
target_part_count = st.number_input('Target Part Count', min_value=0.0, value=st.session_state.target_part_count, format="%.1f", key='target_part_count')
total_parts_made = st.number_input('Total Parts Made', min_value=0.0, value=st.session_state.total_parts_made, format="%.1f", key='total_parts_made')
good_parts = st.number_input('Good Parts', min_value=0.0, max_value=total_parts_made, value=st.session_state.good_parts, format="%.1f", key='good_parts')

# Calculate OEE
if st.button('Calculate OEE'):
    if planned_production == 0 or target_part_count == 0 or total_parts_made == 0:
        st.error('Please enter valid values for all input fields.')
    else:
        availability = (actual_run_time / planned_production) * 100
        performance = (total_parts_made / target_part_count) * 100
        quality = (good_parts / total_parts_made) * 100
        st.write(f'Availability: {availability:.2f}%')
        st.write(f'Performance: {performance:.2f}%')
        st.write(f'Quality: {quality:.2f}%')

        oee = (availability / 100) * (performance / 100) * (quality / 100) * 100
        st.success(f'OEE: {oee:.2f}%')

        # select the area that is affecting the OEE the most
        metrics = ['Availability', 'Performance', 'Quality']
        values = [availability, performance, quality]
        min_index = values.index(min(values))
        st.write(f'The biggest bottleneck is: {metrics[min_index]}')
        
        # Bar Graph for the three factors with the lowest value in red

        data = pd.DataFrame({
            'Metric': ['Availability', 'Performance', 'Quality'],
            'Value': [availability, performance, quality]
        })

        min_value = data['Value'].min()
        data['Color'] = data['Value'].apply(lambda x: 'red' if x == min_value else 'steelblue')

        chart = alt.Chart(data).mark_bar().encode(
            x='Metric',
            y='Value',
            color=alt.Color('Color', scale=None)
        ).properties(
            title='OEE Factors'
        )

        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            font='bold', size=12
        ).encode(
            text=alt.Text('Value:Q', format='.2f')
        )
        st.altair_chart(chart + text, use_container_width=True)


