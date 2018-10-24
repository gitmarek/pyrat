class SampleTime:
    
    def __init__(self, sample_rate=48000, tempo=1, beats_per_measure=4):
        """
        tempo - beats per second
        """

        self._sr = sample_rate
        self._tempo = tempo
        self._bpmeasure = beats_per_measure
        self._update()


    def _update(self):
        
        self._spmin = self._sr*60
        self._sphour= self._spmin*60
        self._spbeat = self._sr / self._tempo
        self._spmeasure = self._bpmeasure * self._spbeat 


    def sample_rate(self, sample_rate=None):
        if sample_rate:
            self._sr = sample_rate
            self._update()
        return self._sr

    def tempo(self, tempo=None):
        if tempo:
            self._tempo = tempo
            self._update()
        return self._tempo

    def beats_per_measure(self, beats_per_measure=None):
        if beats_per_measure:
            self._bpmeasure = beats_per_measure
            self._update()
        return self._bpmeasure


    def beat(self, n=1, measure=0):
        return self._spbeat*n + self._spmeasure*measure 

    def measure(self, n=1):
        return self._spmeasure * n

    def sec(self, n=1):
        return self._sr*n

    def min(self, n=1):
        return self._spmin*n 

    def hour(self, n=1):
        return self._sphour*n
 
    def time(self, sec=1, min=0, hour=0):
        return self.sec(sec) + self.min(min) + self.hour(hour)

