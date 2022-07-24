
import os

test_depot      = ['MA5GEG', 'MA59PF', 'MC9UZT', 'MA7QYE', 'MA9RMH', 'MA6P6Z', 'MA5UK0', 'MA4R9G', 'SF41HU', 'SF5RSR', \
                   'MA9RH9', 'BASF11', '906866', 'HAFX6Q', 'A0MW0M', 'A0YEDL', 'PH6USA', 'MC02EM']

test_indizes    = ['846900', '846741', '720327', '965338', '965814', 'A0AE1X', '969420', '965814']

test_anleihen   = ['450900', 'A0AUXK', '353254', '128531', 'A0T6UH', 'A0BCJ2']

test_etfs       = ['A1C79N', 'A1C79W', 'A2DWM4']

test_edelmetall = ['965515', '965310']

test_currencies = ['965275', 'A0C32V', '965308']

depot_800_share = ['A0NC7B', '906866', 'A14Y6H', 'A14R7U', '918422', '870053', '858144', '864371', '871981', 'A1H5JY', \
                    '866197', '889826', '869964', '865985', '857949']

depot_800_os    = ['JJ2HPH', 'VQ9XQL', 'TT7Z3C', 'JN6FUQ', 'JA30E2']

depot_800_plus  = ['JJ8WC7', 'VQ8M18', 'TT44ZX', 'TT8DRP', 'MA9RMH', 'MA6P6Z', 'MA5UK0', 'MA4R9G', 'SF41HU', 'MA46WY', \
                   'MA9RH9', 'JN0P9E', 'MA9S15', 'MD3WHE', 'MD3HVM']

depot_usa       = ['882807', '930124', 'A0NFQC', 'A1J6Y4', 'A2QQVE']

depot_tsi       = ['840400', '703000', 'KSAG88', 'CBK100', '676650', '660200', '514000', 'UNSE01', 'A2NB60', '703712']

depot_premium   = ['A2NB60', 'KSAG88', 'CBK100', 'A0NFQC', 'A1CX3T', 'A2JG9Z']

depot_test_fonds= ['A0F4Y2', 'A0NEBA', '921826', '980701']

depot_zertifikat= ['SH5LG0', 'KG1DNP']

test0           = ['A0NC7B']

# test0            = ['MA59PF', 'A1CX3T']
# test1            = ['MA59PF', 'BASF11', 'IBM']
# test1            = ['MA59PF', 'US02079K1079', 'BASF11']
# test1            = ['A1CX3T']


depotpath = os.path.join(os.path.dirname(__file__), 'data', 'depots')
print(depotpath)

class Depot():
    def __init__(self, depotname, timestamp, items):
        self.depotname = depotname
        self.timestamp = timestamp
        self.items = items

    def Read(self):
        pass





