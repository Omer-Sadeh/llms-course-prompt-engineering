import runpy
import sys
from unittest.mock import MagicMock, patch

import pandas as pd


class TestDashboard:
    
    def test_dashboard_execution(self):
        # We patch everything needed for the dashboard script
        with patch('streamlit.set_page_config'), \
             patch('streamlit.title'), \
             patch('streamlit.markdown'), \
             patch('streamlit.header'), \
             patch('streamlit.subheader'), \
             patch('streamlit.sidebar') as mock_sidebar, \
             patch('streamlit.dataframe'), \
             patch('streamlit.pyplot'), \
             patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
             patch('pandas.read_csv') as mock_read_csv, \
             patch('src.config.config.config.paths.results') as mock_results_path, \
             patch('matplotlib.pyplot.subplots', return_value=(MagicMock(), MagicMock())), \
             patch('seaborn.barplot'), \
             patch('seaborn.violinplot'):

            mock_results_path.exists.return_value = True
            
            # Mock selectbox return value for metric selection
            mock_sidebar.selectbox.return_value = "vector_distance"

            # Mock Data
            df = pd.DataFrame({
                'strategy': ['A', 'A', 'B', 'B'],
                'vector_distance': [0.1, 0.2, 0.3, 0.4],
                'latency': [1.0, 1.1, 1.2, 1.3]
            })
            mock_read_csv.return_value = df

            # We need to ensure src is in path
            if 'src.dashboard' in sys.modules:
                del sys.modules['src.dashboard']

            # Execute the script
            runpy.run_module('src.dashboard', run_name="__main__")

    def test_dashboard_no_results(self):
         with patch('streamlit.error') as mock_error, \
              patch('streamlit.stop') as mock_stop, \
              patch('streamlit.set_page_config'), \
              patch('streamlit.title'), \
              patch('streamlit.markdown'), \
              patch('src.config.config.config.paths.results') as mock_results_path:
            
            mock_results_path.exists.return_value = False
            mock_stop.side_effect = SystemExit # Simulate stop
            
            if 'src.dashboard' in sys.modules:
                del sys.modules['src.dashboard']
                
            try:
                runpy.run_module('src.dashboard', run_name="__main__")
            except SystemExit:
                pass
                
            mock_error.assert_called()
            mock_stop.assert_called()