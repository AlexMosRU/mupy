import music21
import numpy as np


class Xnote:
    """
    """
    def __init__(self, note, scale_intervals, root, context=None):    
        self.step = self.getStep(note, self.getFullScale(scale_intervals, root))
        self.length = note.fullName.split()[-2]
        
        
    def getFullScale(self, scale_intervals, root):
        net = music21.scale.intervalNetwork.IntervalNetwork()
        net.fillBiDirectedEdges(scale_intervals)
        octaves = [x for x in range(9)]
        notes = []
        for octave in octaves:
            current_root = root.name + str(octave)
            for p in net.realizePitch(current_root):
                if str(p) not in notes:
                    notes.append(str(p))
        return np.array(notes)


    def getStep(self, note, fullScale):
        if note.nameWithOctave in fullScale:
            return np.where(fullScale==note.nameWithOctave)[0][0]
        note_midi = note.pitch.midi
        demNote = music21.note.Note(note_midi - 1)
        if demNote.nameWithOctave in fullScale:
            return np.where(fullScale==demNote.nameWithOctave)[0][0] + 0.5
        accNote = music21.note.Note(note_midi + 1)
        if accNote.nameWithOctave in fullScale:
            return np.where(fullScale==accNote.nameWithOctave)[0][0] - 0.5

        
    def getNote(self, scale_intervals, root):
        noteName = self.getFullScale(scale_intervals, root)[self.step]
        note = music21.note.Note(noteName)
        note.duration = music21.duration.Duration(self.length.lower())
        return note


class Xmotive:
    """
    """
    def __init__(self, xnotes):
        self.notes = xnotes
        
        
    def getNotes(self, scale_intervals, root):
        return [note.getNote(scale_intervals, root) for note in self.notes]
    
    
    def getSteps(self):
        return [note.step for note in self.notes]
    
    
    def getRhythm(self):
        return [note.length for note in self.notes]
    
    
    def getMelodyLine(self):
        line = []
        steps = self.getSteps()
        for n, step in enumerate(steps[1:]):
            line.append(step - steps[n])
        return line
    
    
    def getMidiLine(self, scale_intervals, root):
        line = []
        midi = [x.pitch.midi for x in self.getNotes(scale_intervals, root)]
        for n, step in enumerate(midi[1:]):
            line.append(step - midi[n])
        return line
    
    
class XMotiveTransform():
    """
    """
    def __init__(self, motiveA, motiveB):
        self.stepTransform = []
        self.rhythmTransform = []
        
        aSteps = motiveA.getSteps()
        bSteps = motiveB.getSteps()
        
        for n, a in enumerate(aSteps):
            self.stepTransform.append(a - bSteps[n])
            
        aRhythm = motiveA.getRhythm()
        bRhythm = motiveB.getRhythm()
        
        aLength = [music21.duration.Duration(q.lower()).quarterLength for q in aRhythm]
        bLength = [music21.duration.Duration(q.lower()).quarterLength for q in bRhythm]
        
        for n, a in enumerate(aLength):
            self.rhythmTransform.append(a/bLength[n])