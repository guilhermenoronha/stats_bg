from unittest.mock import patch
from stats_bg.utils import timeit


@patch("stats_bg.utils.logging.info")
@patch("stats_bg.utils.time.perf_counter")
def test_timeit_logs_execution_time(mock_perf_counter, mock_logging_info):
    mock_perf_counter.side_effect = [1.0, 3.0]

    @timeit
    def sample_function(x, y):
        return x + y

    result = sample_function(2, 3)

    assert result == 5
    assert mock_perf_counter.call_count == 2
    mock_logging_info.assert_called_once()

    log_message = mock_logging_info.call_args[0][0]
    assert "Function sample_function took 2.00 seconds" in log_message