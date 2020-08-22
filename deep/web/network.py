 #tr
import numpy as np
from keras import models, layers, optimizers
from keras.utils import to_categorical
import csv
from datetime import datetime

def now_time():
    return datetime.now().strftime('%H:%m:%S')

class Network:
    folder = r'../../'
    network = None
    npa = None
    npb = None
    npi = None
    npt = None
    inited = False
    test_csv_file = open('../../test.csv', 'r')
    test_csv_reader = csv.reader(test_csv_file)
    last82 = []
    head82 = ['MachineIdentifier',
 'ProductName',
 'EngineVersion',
 'AppVersion',
 'AvSigVersion',
 'IsBeta',
 'RtpStateBitfield',
 'IsSxsPassiveMode',
 'DefaultBrowsersIdentifier',
 'AVProductStatesIdentifier',
 'AVProductsInstalled',
 'AVProductsEnabled',
 'HasTpm',
 'CountryIdentifier',
 'CityIdentifier',
 'OrganizationIdentifier',
 'GeoNameIdentifier',
 'LocaleEnglishNameIdentifier',
 'Platform',
 'Processor',
 'OsVer',
 'OsBuild',
 'OsSuite',
 'OsPlatformSubRelease',
 'OsBuildLab',
 'SkuEdition',
 'IsProtected',
 'AutoSampleOptIn',
 'PuaMode',
 'SMode',
 'IeVerIdentifier',
 'SmartScreen',
 'Firewall',
 'UacLuaenable',
 'Census_MDC2FormFactor',
 'Census_DeviceFamily',
 'Census_OEMNameIdentifier',
 'Census_OEMModelIdentifier',
 'Census_ProcessorCoreCount',
 'Census_ProcessorManufacturerIdentifier',
 'Census_ProcessorModelIdentifier',
 'Census_ProcessorClass',
 'Census_PrimaryDiskTotalCapacity',
 'Census_PrimaryDiskTypeName',
 'Census_SystemVolumeTotalCapacity',
 'Census_HasOpticalDiskDrive',
 'Census_TotalPhysicalRAM',
 'Census_ChassisTypeName',
 'Census_InternalPrimaryDiagonalDisplaySizeInInches',
 'Census_InternalPrimaryDisplayResolutionHorizontal',
 'Census_InternalPrimaryDisplayResolutionVertical',
 'Census_PowerPlatformRoleName',
 'Census_InternalBatteryType',
 'Census_InternalBatteryNumberOfCharges',
 'Census_OSVersion',
 'Census_OSArchitecture',
 'Census_OSBranch',
 'Census_OSBuildNumber',
 'Census_OSBuildRevision',
 'Census_OSEdition',
 'Census_OSSkuName',
 'Census_OSInstallTypeName',
 'Census_OSInstallLanguageIdentifier',
 'Census_OSUILocaleIdentifier',
 'Census_OSWUAutoUpdateOptionsName',
 'Census_IsPortableOperatingSystem',
 'Census_GenuineStateName',
 'Census_ActivationChannel',
 'Census_IsFlightingInternal',
 'Census_IsFlightsDisabled',
 'Census_FlightRing',
 'Census_ThresholdOptIn',
 'Census_FirmwareManufacturerIdentifier',
 'Census_FirmwareVersionIdentifier',
 'Census_IsSecureBootEnabled',
 'Census_IsWIMBootEnabled',
 'Census_IsVirtualDevice',
 'Census_IsTouchEnabled',
 'Census_IsPenCapable',
 'Census_IsAlwaysOnAlwaysConnectedCapable',
 'Wdft_IsGamer',
 'Wdft_RegionIdentifier']

    def init(self):
        if not self.inited:
            self.load_np('npa100k.npy', 'npi100k.npy')
            self.load_tst('npa100k_t.npy', 'npi100k_t.npy')
            self.make_net2()
        self.inited = True
        print('app inited')

    def read_test_line(self):
        if not self.inited:
            self.init()
        record = []
        offset = self.test_csv_reader.line_num
        for e in self.test_csv_reader:
            self.last82 = e
            record.append(e[0])
            record.append(e[1])
            record.append(e[18])
            record.append(e[80])
            break
        record.append(now_time())
        vanga = self.predict(1, offset)
        record.append(vanga[0][1])
        return record

    def get_playbook(self):
        s = ''
        with open('playbook.txt', 'r') as f:
            for line in f.readlines():
                s += line + '\n'
        return s

    def get_full_info(self):
        s = ''
        i = 0
        for line in self.last82:
            s += self.head82[i] + ': ' + line + '\n'
            i += 1
        return s

    def make_net2(self, weights_file = './results/netw7.weights'):
        self.make_net()
        #fit(network, npa, npi)
        self.network.load_weights(weights_file)

    def load_np(self, arr = 'train2.npy', ari = 'train2_i.npy'):
        self.npa = np.load(self.folder + arr)
        self.npi = np.load(self.folder + ari)
        self.npb = to_categorical(self.npi)
        
    def load_tst(self, arr = 'train2_test.npy', ari = 'train2_i_test.npy'):
        self.npa_t = np.load(self.folder + arr)
        self.npi_t = to_categorical( np.load(self.folder + ari) )

    def shuffle(self):
        npx = np.arange(len(self.npi))
        np.random.shuffle(npx)
        self.npa = self.npa[npx]
        self.npi = self.npi[npx]

    def make_net(self):
        self.network = models.Sequential()
        self.network.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
                    input_shape=(len(self.npa[0]),))) # 81, 106
        self.network.add(layers.Dense(1024, activation='relu'))
        self.network.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True))
        self.network.add(layers.Dense(256, activation='relu'))
        self.network.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True))
        self.network.add(layers.Dense(2, activation='softmax'))
        self.network.compile(optimizer='rmsprop',
                        loss = 'categorical_crossentropy',
                        metrics = ['accuracy'])
        

    def fit(self):
        self.network.fit(npa, npb, epochs=5, batch_size=128)

    def train(self, rms = 0.001):
        #rms /= 2.0
        print("RMSprop: lr =", rms)
        self.network.compile(optimizer=optimizers.RMSprop(lr=rms),
                    loss = 'categorical_crossentropy',
                    metrics = ['accuracy'])
        #npa, npi = shuffle(npa, npi)
        self.network.fit(self.npa, self.npb, epochs=1, batch_size=128)
        self.network.save_weights('netw7+'+str(rms)+'.weights')

    def evalute(self, npx, npy):
        self.loss, self.acc = network.evaluate(npx, npy)

    def predict(self, count = 1000, offset = 0, npx = None):
        if npx is None:
            if self.npt is None:
                self.npt = np.load(self.folder +r'test3.npy')
            npx = self.npt
        n = len(npx) - 1
        if count <= 0 or count > n:
            count = n
        output_array_i = self.network.predict(npx[offset : offset + count])
        return output_array_i # second number - attack %

    def save(self, npx, filename = r'test3_i_gen.npy'):
        np.save(self.folder + filename, npx)


