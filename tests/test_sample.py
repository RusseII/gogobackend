import sys
import pytest
from mock import Mock
sys.path.append('.')
from engine.parse_files import ParseData
from engine.send_emails import HandleEmail


class TestParseData():
    pd = ParseData()

    def test_find_emails(self):
        assert (self.pd.find_emails('tests/resumes/julie.doc') == [
            "jha12@zips.uakron.edu"
        ])
        assert (self.pd.find_emails('tests/resumes/kyle.docx') == [
            "Kjv13@zips.uakron.edu"
        ])
        assert (self.pd.find_emails('tests/resumes/russell.pdf') == [
            "Rwr21@zips.uakron.edu"
        ])
        assert (self.pd.find_emails(
            'tests/resumes/emails_test_find_emails.csv') == [
                "rwr21@zips.uakron.edu", "rwr21@zips.uakron.edu"
            ])


class TestSendGrid():
    hd = HandleEmail()

    @pytest.fixture
    def mock_send_grid(self):
        return Mock(spec=HandleEmail)

    def test_mock(self, mock_send_grid):
        mock_send_grid.send("rwr21@zips.uakron.edu")

    # @mock.patch('engine.send_emails.')
    # def test_send_grid(self):
