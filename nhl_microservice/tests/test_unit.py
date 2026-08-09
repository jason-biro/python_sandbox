from scraper import _parse_html_page

def test_parse_html_page_handles_valid_structures():
    """Validates that valid team rows are parsed correctly into raw dictionary arrays."""
    mock_html = """
    <table>
        <tr class="team">
            <td class="name">Some Team</td>
            <td class="year">1990</td>
            <td class="wins">50</td>
            <td class="losses">32</td>
            <td class="pct">0.610</td>
        </tr>
    </table>
    """
    results = _parse_html_page(mock_html)

    assert len(results) == 1
    assert results[0]["team_name"] == "Some Team"
    assert results[0]["year"] == 1990
    assert results[0]["wins"] == 50

def test_parse_html_age_ignores_malformed_structures():
    """Ensures parsing exceptions are handled safely without raising errors."""
    mock_malformed_html = """
    <table>
        <tr class="team">
            <td class="name">Broken Team</td>
            <td class="year">NotAYear</td>
        </tr>
    </table>
    """
    results = _parse_html_page(mock_malformed_html)
    assert len(results) == 0
