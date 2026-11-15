"""Local HEMS experiment dashboard. Start with streamlit run."""
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from hems_sim.experiments import run_experiment, saved_runs

st.set_page_config(page_title='HEMS Simulator', page_icon='🏠', layout='wide')
st.title('HEMS Simulator')
st.caption('Custom Alameda • CityLearn 3.2.0 • Reproducible fixed-action experiments')

with st.sidebar:
    st.header('New experiment')
    with st.form('experiment'):
        scenario = st.selectbox('Scenario', ['Custom Alameda', 'Frozen thermal scenario'])
        start = st.number_input('Start simulation hour', 0, 8758, 0)
        steps = st.number_input('Transitions (hours)', 1, 8759, 48)
        seed = st.number_input('Random seed', 0, 2147483647, 2022)
        hvac = st.slider('HVAC action', -1.0, 1.0, 0.2, 0.05)
        st.caption('Positive: heating · Negative: cooling. Battery and EV actions remain zero.')
        submitted = st.form_submit_button('Run experiment', type='primary')
    st.link_button('Open CityLearn results viewer', 'https://citylearnui.netlify.app/')

if submitted:
    try:
        with st.spinner('Running simulator and exporting results…'):
            path = run_experiment(int(start), int(steps), hvac, int(seed), scenario.startswith('Frozen'))
        st.session_state['selected_run'] = str(path)
        st.success('Experiment saved.')
    except Exception as exc:
        st.error(f'Experiment failed: {exc}')

paths = saved_runs()
if not paths:
    st.info('Run your first experiment using the sidebar. Results and CityLearn CSV exports are saved separately for each run.')
    st.stop()
options = [str(path) for path in paths]
if st.session_state.get('selected_run') not in options:
    st.session_state['selected_run'] = options[0]
selected = st.selectbox('Saved experiment', options, format_func=lambda p: p.replace('\\', '/').split('/')[-2], key='selected_run')
with open(selected, encoding='utf-8') as file:
    result = json.load(file)
rows = result['rows']
config = result['configuration']
st.caption(f"Scenario: {result['scenario']} · Seed: {config['random_seed']} · HVAC: {result['hvac_action']:+.2f}")
a, b, c = st.columns(3)
a.metric('Transitions', len(rows))
b.metric('Final observed indoor temperature', f"{rows[-1]['observed_temperature_C']:.2f} °C")
c.metric('Dynamic control transitions', sum(row['dynamic'] for row in rows))
st.info('The first 14 transitions build thermal history. Charts use simulation-hour indices, not verified calendar dates. Observation values are shown at the next observation step.')


def frame(payload):
    names = payload['observation_names'][0]
    records = []
    for row in payload['rows']:
        record = dict(zip(names, row['observations'][0]))
        record['Simulation hour'] = row['controlled_global_step'] + 1
        record['Dynamic control'] = row['dynamic']
        records.append(record)
    return pd.DataFrame(records)


data = frame(result)
signals = result['observation_names'][0]
signal = st.selectbox('Signal', signals, index=signals.index('indoor_dry_bulb_temperature'), key='signal')
comparison = st.selectbox('Compare with', ['None'] + [p for p in options if p != selected],
                          format_func=lambda p: p if p == 'None' else p.replace('\\', '/').split('/')[-2], key='comparison')
chart_data = data[['Simulation hour', signal]].copy()
chart_data['Run'] = result['run_id']
if comparison != 'None':
    with open(comparison, encoding='utf-8') as file:
        other = json.load(file)
    keys = ['simulation_start_time_step', 'simulation_end_time_step', 'random_seed', 'building_id']
    if other['scenario'] != result['scenario'] or any(other['configuration'][k] != config[k] for k in keys):
        st.warning('These runs differ in scenario, window, building, or seed. Interpret their comparison accordingly.')
    other_data = frame(other)
    if signal in other_data:
        extra = other_data[['Simulation hour', signal]].copy()
        extra['Run'] = other['run_id']
        chart_data = pd.concat([chart_data, extra], ignore_index=True)
figure = px.line(chart_data, x='Simulation hour', y=signal, color='Run')
warmup = data.loc[~data['Dynamic control'], 'Simulation hour']
if not warmup.empty:
    figure.add_vrect(x0=float(warmup.min()) - 1, x1=float(warmup.max()),
                    fillcolor='gray', opacity=0.12, line_width=0, annotation_text='Thermal warm-up')
st.plotly_chart(figure, width='stretch')
temperature_columns = ['indoor_dry_bulb_temperature', 'outdoor_dry_bulb_temperature',
                       'indoor_dry_bulb_temperature_heating_set_point', 'indoor_dry_bulb_temperature_cooling_set_point']
st.subheader('Temperature and set points')
st.plotly_chart(px.line(data, x='Simulation hour', y=[x for x in temperature_columns if x in data],
                        labels={'value': 'Temperature (°C)', 'variable': 'Signal'}), width='stretch')
with st.expander('Observations and configuration'):
    st.dataframe(data, width='stretch')
    st.json(config)
st.download_button('Download observations CSV', data.to_csv(index=False), file_name=f"{result['run_id']}.csv", mime='text/csv')
st.download_button('Download complete run JSON', json.dumps(result, indent=2), file_name=f"{result['run_id']}.json", mime='application/json')
st.download_button('Download interactive chart', figure.to_html(include_plotlyjs=True), file_name=f"{result['run_id']}.html", mime='text/html')
st.caption('For native KPIs and component charts, open CityLearn UI, choose folders, and select:')
st.code(result['export_directory'], language=None)
