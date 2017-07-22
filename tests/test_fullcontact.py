import sys
sys.path.append('.')
from engine.full_contact import FullContact


class TestFullContact():
    fc = FullContact('test')

    def test_lookup_company_update(self):
        fullcontact_info = self.fc.lookup_company_update('596eea8e9b4d3900087c2d58')
        assert fullcontact_info['website'] == "https://www.fullcontact.com"

