import streamlit as st
import pandas as pd
import altair as alt

st.title('OEE Calculator')

# Input fields
planned_production = st.number_input('Planned production time', min_value=0.0, value=0.0, format="%.1f")
actual_run_time = st.number_input('Actual Run Time', min_value=0.0, value=0.0, format="%.1f")
target_part_count = st.number_input('Target Part Count', min_value=0.0, value=0.0, format="%.1f")
total_parts_made = st.number_input('Total Parts Made', min_value=0.0, value=0.0, format="%.1f")
good_parts = st.number_input('Good Parts', min_value=0.0, max_value=total_parts_made, value=0.0, format="%.1f")

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
            text='Value:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)
