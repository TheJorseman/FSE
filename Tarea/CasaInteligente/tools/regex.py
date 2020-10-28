
class regexp(object):
    @staticmethod
    def get_csv():
        return "\s*(.+?)(?:,|$)"

    @staticmethod
    def disp_with_number_0_1():
        return "\s+(\w*)\s+([0].\d|[1,0].[0]|[1,0])"

    def get_csv_numbers(self):
        pass
