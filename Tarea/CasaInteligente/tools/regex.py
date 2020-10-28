
class regexp(object):
    @staticmethod
    def get_csv():
        return "\s*(.+?)(?:,|$)"
    
    def get_csv_numbers(self):
        pass