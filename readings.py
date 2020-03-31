import csv


#repr = 'Sensor data: t={}, flow ={}, pressure1 ={} [pa], pressure2 ={} [pa], oxygen: ={} %'.format(
#            self.timestamp,
#            self.flow,
#            self.pressure_1_pa,
#            self.pressure_2_pa,
#            self.oxygen)

class Readings():
    def __init__(self, time, S_freq, S_pressure1, S_pressure2, S_oxygen):
        self.time = float(time)
        self.S_freq = float(S_freq)
        self.S_pressure1 = float(S_pressure1)
        self.S_pressure2 = float(S_pressure1)
        self.S_oxygen = int(S_oxygen)
        self.counter1 = 0
        self.counter2 = 0
    

    def proces_input(self, text):
        if text.startswith(b'###'):
           sensorArray = [float(s) for s in str.split() if s.isdigit()]
        else:
            print("error in reading sensordata")
            return
        self.time = sensorArray[0]
        self.freq = sensorArray[1]
        self.pressure1 = sensorArray[2]
        self.pressure2 = sensorArray[3]
        self.oxygen = sensorArray[4]
        write_file(self, sensorArray)
        
    def write_file(self, sensorArray):
        f = open('measurements'+self.counter2+'.csv','w')
        with f:
            writer = csv.writer(f)
            writer.writerow(sesorArray)
        self.counter1 = self.counter1 + 1
        if self.counter1 == 60000:
            self.counter1 = 0
            self.counter2 = self.counter2 + 1
        
        
        

    

