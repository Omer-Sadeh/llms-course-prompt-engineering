import pytest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import pandas as pd

# We need to mock streamlit BEFORE importing dashboard, 
# but dashboard is imported inside the test function usually or we patch sys.modules.
# However, the dashboard script runs at top level when imported. 
# So we should probably test it by executing it via runpy or just importing it after patching.

# Strategy: Patch sys.modules to mock streamlit, then import src.dashboard
# Or better: use patch.dict on sys.modules.

class TestDashboard:
    
    @pytest.fixture
    def mock_streamlit(self):
        with patch.dict(sys.modules, {'streamlit': MagicMock()}):
            yield sys.modules['streamlit']

    def test_dashboard_execution(self):
        # Mock dependencies
        with patch('streamlit.set_page_config'), \
             patch('streamlit.title'), \
             patch('streamlit.markdown'), \
             patch('streamlit.header'), \
             patch('streamlit.subheader'), \
             patch('streamlit.sidebar'), \
             patch('streamlit.dataframe'), \
             patch('streamlit.pyplot'), \
             patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
             patch('pandas.read_csv') as mock_read_csv, \
             patch('src.config.config.config.paths.results') as mock_results_path, \
             patch('matplotlib.pyplot.subplots', return_value=(MagicMock(), MagicMock())), \
             patch('seaborn.barplot'), \
             patch('seaborn.violinplot'):
            
            # Setup mocks
            mock_results_path.exists.return_value = True
            
            # Mock Data
            df = pd.DataFrame({
                'strategy': ['A', 'A', 'B', 'B'],
                'vector_distance': [0.1, 0.2, 0.3, 0.4]
            })
            mock_read_csv.return_value = df
            
            # Since dashboard.py is a script that runs on import, we need to reload it or run it.
            # Using runpy is safer for scripts.
            import runpy
            
            # We need to ensure src is in path (it is added in the script, but for test environment)
            if 'src.dashboard' in sys.modules:
                del sys.modules['src.dashboard']
            
            # Execute the script
            runpy.run_module('src.dashboard', run_name="__main__")
            
            # Verify calls
            # We can't easily verify calls on the module level mocks unless we keep a reference to them
            # but verifying it ran without exception is a good start.

    def test_dashboard_no_results(self):
         with patch('streamlit.error') as mock_error, \
              patch('streamlit.stop') as mock_stop, \
              patch('src.config.config.config.paths.results') as mock_results_path:
            
            mock_results_path.exists.return_value = False
            
            import runpy
            if 'src.dashboard' in sys.modules:
                del sys.modules['src.dashboard']
                
            try:
                runpy.run_module('src.dashboard', run_name="__main__")
            except SystemExit:
                pass
            except Exception:
                pass # mocking stop might cause exception if not handled
                
            mock_error.assert_called()
            mock_stop.assert_called()

