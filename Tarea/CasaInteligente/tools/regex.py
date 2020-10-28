
class regexp(object):
    @staticmethod
    def get_csv(self):
        return "\s*(.+?)(?:,|$)"
    
    def get_csv_numbers(self):
        pass